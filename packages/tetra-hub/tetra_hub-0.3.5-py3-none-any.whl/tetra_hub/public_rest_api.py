from __future__ import annotations
import datetime
import os
import json
import threading
from typing import Any, Dict, List, Optional, OrderedDict, Tuple, Union
from urllib.parse import urljoin
import posixpath
import requests
import configparser
from tqdm import tqdm
from contextlib import nullcontext
from dataclasses import dataclass
from types import SimpleNamespace
from typing import List
import numpy as np
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from . import public_api_pb2 as api_pb
from . import api_status_codes
from pathlib import Path
import tempfile
from zipfile import ZipFile

UNKNOWN_ERROR = "Unknown error."
API_VERSION = "v1"

# Used for error message feedback
CASUAL_CLASSNAMES = {
    api_pb.ProfileJob: "job",
    api_pb.Model: "model",
    api_pb.User: "user",
}

DEFAULT_CONFIG_PATH = "~/.tetra/client.ini"

Shapes = Union[
    List[Tuple[int, ...]],
    OrderedDict[str, Tuple[int, ...]],
    List[Tuple[str, Tuple[int, ...]]],
    Dict[str, Tuple[int, ...]],
]

DatasetEntries = Union[
    OrderedDict[str, List[np.ndarray]],
    OrderedDict[str, np.ndarray],
    Dict[str, List[np.ndarray]],
    Dict[str, np.ndarray],
]


def get_config_path(expanduser=True):
    path = os.environ.get("TETRA_CLIENT_INI", DEFAULT_CONFIG_PATH)
    if expanduser:
        path = os.path.expanduser(path)
    return path


@dataclass
class ClientConfig:
    """
    Configuration information, such as your API token, for use with
    :py:class:`.Client`.

    Parameters
    ----------
    api_url
        URL of the API backend endpoint.
    web_url
        URL of the web interface.
    api_token
        API token. Available through the web interface under the "Account" page.
    """

    api_url: str
    web_url: str
    api_token: str


class APIException(Exception):
    """
    Exception for the python REST API.

    Parameters
    ----------
    message : str
        Message of the failure. If None, sets it automatically based on
        `status_code`.
    status_code : int
        API status code (a superset of HTTP status codes).
    """

    def __init__(self, message=None, status_code=None):
        if message is None:
            if status_code is not None:
                # Some common error codes have custom messages
                if status_code == api_status_codes.HTTP_401_UNAUTHORIZED:
                    message = "API authentication failure; please check your API token."
                elif status_code == api_status_codes.HTTP_429_TOO_MANY_REQUESTS:
                    message = "Too Many Requests: please slow down and try again soon."
                elif status_code == api_status_codes.API_CONFIGURATION_MISSING_FIELDS:
                    config_path = get_config_path(expanduser=False)
                    message = f"Required fields are missing from your {config_path}."
                elif status_code == api_status_codes.HTTP_413_REQUEST_ENTITY_TOO_LARGE:
                    message = "The uploaded asset is too large. Please contact us for workarounds."
                else:
                    message = f"API request returned status code {status_code}."
            else:
                message = UNKNOWN_ERROR

        super().__init__(message)
        self.status_code = status_code


def _response_as_protobuf(
    response: requests.Response, protobuf_class: Any, obj_id: Optional[int] = None
) -> Any:
    if (
        api_status_codes.is_success(response.status_code)
        and response.headers.get("Content-Type") == "application/x-protobuf"
    ):
        pb = protobuf_class()
        pb.ParseFromString(response.content)
        return pb
    elif (
        response.status_code == api_status_codes.HTTP_404_NOT_FOUND
        and obj_id is not None
    ):
        prefix = ""
        class_name = CASUAL_CLASSNAMES.get(protobuf_class)
        if class_name is not None:
            prefix = class_name.capitalize() + " "

        raise APIException(
            f"{prefix}ID {obj_id} could not be found. It may not exist or you may not have permission to view it.",
            status_code=response.status_code,
        )
    else:
        raise APIException(status_code=response.status_code)


def _prepare_offset_limit_query_list(offset: int, limit: Optional[int]) -> List[str]:
    extras = []
    if offset > 0:
        extras.append(f"offset={offset}")
    if limit is not None:
        extras.append(f"limit={limit}")
    return extras


def _prepare_offset_limit_query(offset: int, limit: Optional[int]) -> str:
    extras = _prepare_offset_limit_query_list(offset, limit)
    if extras:
        return "?" + "&".join(extras)
    else:
        return ""


def _load_default_api_config(verbose=False) -> ClientConfig:
    """
    Load a default ClientConfig from default locations.

    Parameters
    ----------
    verbose : bool
        Print where config file is loaded from.

    Returns
    -------
    config : ClientConfig
        API authentication configuration.
    """
    # Load from default config path
    config = configparser.ConfigParser()
    # Client config should be in ~/.tetra/client.ini
    tilde_config_path = get_config_path(expanduser=False)
    config_path = os.path.expanduser(tilde_config_path)
    if verbose:
        print(f"Loading Client config from {tilde_config_path} ...")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"{tilde_config_path} not found. Please go to the Account page to "
            "find instructions of how to install your API key."
        )
    config.read([config_path])
    try:
        client_config = config["api"]

        api_config = ClientConfig(
            api_url=client_config["api_url"],
            web_url=client_config["web_url"],
            api_token=client_config["api_token"],
        )
    except KeyError:
        raise APIException(
            status_code=api_status_codes.API_CONFIGURATION_MISSING_FIELDS
        )
    return api_config


def _auth_header(
    config: ClientConfig, content_type: str = "application/x-protobuf"
) -> dict:
    header = {
        "Authorization": f"token {config.api_token}",
        "Content-Type": content_type,
    }
    return header


def _api_url(config: ClientConfig, *rel_paths) -> str:
    return urljoin(config.api_url, posixpath.join("api", API_VERSION, *rel_paths, ""))


def _get_token(api_url, email, password):
    url = urljoin(
        api_url, posixpath.join("api", API_VERSION, "users", "auth", "login", "")
    )
    data = {"email": email, "password": password}
    header = {"Content-Type": "application/json"}
    response = requests.post(url, headers=header, data=json.dumps(data))
    if api_status_codes.is_success(response.status_code):
        return json.loads(response.content)["key"]
    elif response.status_code == 400:
        raise ValueError("Failed to log in: Wrong Username / Password")
    else:
        raise APIException(status_code=response.status_code)


def _create_named_tensor(name: str, shape: Tuple[int, ...]) -> api_pb.NamedTensorType:
    tensor_type_list = []
    for i in shape:
        tensor_type_list.append(i)
    tensor_type_pb = api_pb.TensorType(
        shape=tensor_type_list, dtype=api_pb.TensorDtype.TENSOR_DTYPE_FLOAT32
    )
    return api_pb.NamedTensorType(name=name, tensor_type=tensor_type_pb)


def _list_shapes_to_tensor_type_list_pb(
    input_shapes: Shapes,
) -> api_pb.NamedTensorTypeList:

    tensor_type_pb_list = []

    if isinstance(input_shapes, dict):
        input_shapes = OrderedDict(sorted(input_shapes.items()))
        if isinstance(input_shapes, OrderedDict):
            for name, shape in input_shapes.items():
                named_tensor_type_pb = _create_named_tensor(name, shape)
                tensor_type_pb_list.append(named_tensor_type_pb)
    if isinstance(input_shapes, list):
        if isinstance(input_shapes[0][0], int):
            for index, shape in enumerate(input_shapes):
                named_tensor_type_pb = _create_named_tensor(
                    f"input_{index+1}", shape  # type: ignore
                )
                tensor_type_pb_list.append(named_tensor_type_pb)
        else:
            for name_and_shape in input_shapes:
                name, shape = name_and_shape
                named_tensor_type_pb = _create_named_tensor(name, shape)  # type: ignore
                tensor_type_pb_list.append(named_tensor_type_pb)

    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _tensor_type_list_pb_to_list_shapes(
    tensor_type_list_pb: api_pb.NamedTensorTypeList,
) -> List[Tuple[str, Tuple[int, ...]]]:
    shapes_list = []
    for named_tensor_type in tensor_type_list_pb.types:
        shape = []
        for d in named_tensor_type.tensor_type.shape:
            shape.append(d)
        shapes_list.append((named_tensor_type.name, tuple(shape)))
    return shapes_list


_get_unique_path_lock = threading.Lock()


def _get_unique_path(dst_path):
    name, ext = os.path.splitext(dst_path)
    if ext == ".zip":
        name, sub_ext = os.path.splitext(name)
        ext = sub_ext + ext

    _get_unique_path_lock.acquire()
    if os.path.exists(dst_path):
        now = str(datetime.datetime.now().time()).replace(":", ".")
        dst_path = f"{name}_{now}{ext}"

    # Write empty file (to be overwritten later), for thread safety.
    open(dst_path, "a").close()

    _get_unique_path_lock.release()

    name = os.path.basename(dst_path)

    return dst_path, name


def _convert_inputs_to_tensor_type_list_pb(
    inputs: DatasetEntries,
) -> api_pb.NamedTensorTypeList:
    tensor_type_pb_list = []
    for name, tensor in inputs.items():
        named_tensor_type_pb = _create_named_tensor(name, tensor[0].shape)
        tensor_type_pb_list.append(named_tensor_type_pb)
    return api_pb.NamedTensorTypeList(types=tensor_type_pb_list)


def _do_input_shapes_match(
    input_shapes: Shapes,
    tensor_type_list: api_pb.NamedTensorTypeList,
):
    inputs_tensor_type_list = _tensor_type_list_pb_to_list_shapes(tensor_type_list)
    inputs_shapes_tensor_type_list = _tensor_type_list_pb_to_list_shapes(
        _list_shapes_to_tensor_type_list_pb(input_shapes)
    )

    input_names_match = [False] * len(inputs_tensor_type_list)
    for i, (input_name, input_tensor_shape) in enumerate(inputs_tensor_type_list):
        for _, (input_shape_name, input_shape) in enumerate(
            inputs_shapes_tensor_type_list
        ):
            if input_name == input_shape_name:
                input_names_match[i] = True
                if input_tensor_shape != input_shape:
                    return False
    return all(input_names_match)


def _download_file(
    url: str, filename: str, dst_path: str, verbose: bool, extract_model: bool = False
) -> str:
    dst_path = os.path.expanduser(dst_path)  # Expand ~ to user home in path.

    # Unzip model only if extract_model is set and uploaded model is zipped.
    model_to_be_extracted = extract_model and filename.endswith(".zip")

    # If no filename is provided, use the filename given to us by the parent
    if os.path.isdir(dst_path):
        dst_path = os.path.join(dst_path, filename)

        # Append numerical suffix to the filename if the dst file already exists.
        dst_path, filename = _get_unique_path(dst_path)

        # Remove .zip extension from destination path
        if model_to_be_extracted:
            dst_path = os.path.splitext(dst_path)[0]
    elif model_to_be_extracted:
        raise ValueError(
            "Model cannot be extracted to a file. Please provide a directory path."
        )

    # Verify dst parent dir exists. The same error thrown by open() called
    # below would include the model name, which is confusing.
    parent_dir = os.path.dirname(dst_path)
    if parent_dir and not os.path.exists(parent_dir):
        raise ValueError(f"Download directory '{parent_dir}' does not exist.")

    response = requests.get(url, stream=True)
    if api_status_codes.is_success(response.status_code):
        file_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        if verbose:
            tqdm_context = tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=block_size,
                colour="magenta",
                desc=filename,
            )
        else:
            tqdm_context = nullcontext()

        with tqdm_context as progress_bar:
            # Download to a temporary directory first, so if the download
            # fails or is cancelled midway, the user isn't left with a
            # useless partial artifact on disk.
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_dst_path = os.path.join(tmpdir, os.path.basename(dst_path))
                with open(tmp_dst_path, "wb") as fd:
                    for data in response.iter_content(block_size):
                        written_data = fd.write(data)
                        if progress_bar:
                            progress_bar.update(written_data)

                if model_to_be_extracted:
                    with ZipFile(tmp_dst_path, "r") as zippedModel:
                        zippedModel.extractall(dst_path)
                    os.remove(tmp_dst_path)
                else:
                    # Cannot use os.rename, whose doc string states: "On
                    # Windows, if dst exists a FileExistsError is always
                    # raised." `dst_path` is always created by
                    # `_get_unique_path`
                    os.replace(tmp_dst_path, dst_path)
    else:
        raise APIException(status_code=response.status_code)

    return dst_path


# These helper functions are placed in a utils namespace
# so as not to confuse with core API functions
utils = SimpleNamespace(
    response_as_protobuf=_response_as_protobuf,
    prepare_offset_limit_query=_prepare_offset_limit_query,
    prepare_offset_limit_query_list=_prepare_offset_limit_query_list,
    load_default_api_config=_load_default_api_config,
    auth_header=_auth_header,
    api_url=_api_url,
    list_shapes_to_tensor_type_list_pb=_list_shapes_to_tensor_type_list_pb,
    tensor_type_list_pb_to_list_shapes=_tensor_type_list_pb_to_list_shapes,
    get_unique_path=_get_unique_path,
    download_file=_download_file,
    convert_inputs_to_tensor_type_list_pb=_convert_inputs_to_tensor_type_list_pb,
    do_input_shapes_match=_do_input_shapes_match,
)


def get_auth_user(config: ClientConfig) -> api_pb.User:
    """
    Get authenticated user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.

    Returns
    -------
    user_pb : User
        Get authenticated user information.
    """
    url = utils.api_url(config, "users", "auth", "user")
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    # Note, the API returns a JSON right now, but we will translate this to a
    # protobuf
    content = json.loads(response.content)
    if api_status_codes.is_success(response.status_code):
        user_pb = api_pb.User(
            id=content["pk"],
            first_name=content.get("first_name", ""),
            last_name=content.get("last_name", ""),
            email=content["email"],
        )
        return user_pb
    else:
        raise APIException(status_code=response.status_code)


def get_user(config: ClientConfig, user_id: int) -> api_pb.User:
    """
    Get user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    user_id : int
        User ID.

    Returns
    -------
    user_pb : User
       User information as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "users", str(user_id))
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.User, obj_id=user_id)


def get_user_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.UserList:
    """
    Get user information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    user_list_pb : UserList
       User list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "users")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.UserList)


def get_device_list(
    config: ClientConfig,
    name: str = "",
    os: str = "",
    attributes: List[str] = [],
    select: bool = False,
) -> api_pb.DeviceList:
    """
    Get list of active devices.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Only devices with this exact name will be returned.
    os : str
        Only devices with an OS version that is compatible with this os are returned
    attributes : List[str]
        Only devices that have all requested properties are returned.
    select: bool
        whether to return a list or a single device

    Returns
    -------
    device_list_pb : DeviceList
       Device list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "devices")
    url += f"?name={name}&os={os}&select={select}"
    for attr in attributes:
        url += f"&attributes={attr}"
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DeviceList)


def create_profile_job(
    config: ClientConfig, profile_job_pb: api_pb.ProfileJob
) -> api_pb.CreateUpdateResponse:
    """
    Create new profile job.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_pb : ProfileJob
        Protobuf object with new profile job.

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")
    header = utils.auth_header(config)
    job_pb = api_pb.Job(profile_job=profile_job_pb)
    response = requests.post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    return utils.response_as_protobuf(response, api_pb.CreateUpdateResponse)


def create_validation_job(
    config: ClientConfig, validation_job_pb: api_pb.ValidationJob
) -> api_pb.CreateUpdateResponse:
    """
    Create new validation job.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_pb : ValidationJob
        Protobuf object containing properties for the new validation job

    Returns
    -------
    response_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse. If successful, ``id`` will be nonzero.
        If failure, ``id`` will be zero and ``status`` will contain an error.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")
    header = utils.auth_header(config)
    job_pb = api_pb.Job(validation_job=validation_job_pb)
    response = requests.post(
        url,
        data=job_pb.SerializeToString(),
        headers=header,
    )
    return utils.response_as_protobuf(response, api_pb.CreateUpdateResponse)


def get_job(config: ClientConfig, job_id: str) -> api_pb.Job:
    """
    Get job information.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID.

    Returns
    -------
    job_pb : ProfileJob
        Profile job as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs", job_id)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Job, obj_id=job_id)


def get_job_list(
    config: ClientConfig,
    offset: int = 0,
    limit: int | None = None,
    states: List["api_pb.JobState.ValueType"] = [],
    job_type: "api_pb.JobType.ValueType" = api_pb.JobType.JOB_TYPE_UNSPECIFIED,
) -> api_pb.JobList:
    """
    Get list of jobs visible to the authenticated user.

    Parameters
    ----------
    config :
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.
    states :
        Filter by list of states.
    job_type :
        Filter by job type. JOB_TYPE_UNSPECIFIED will return all jobs.

    Returns
    -------
    list_pb : JobList
        List of jobs as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "jobs")

    # TODO: better API for joining optional query strings.
    query_components = []
    query_components += utils.prepare_offset_limit_query_list(offset, limit)
    if states:
        states_str = ",".join([str(x) for x in states])
        states_query = f"state={states_str}"
        query_components.append(states_query)
    if job_type != api_pb.JobType.JOB_TYPE_UNSPECIFIED:
        job_type_query = f"type={job_type}"
        query_components.append(job_type_query)
    if query_components:
        url += "?" + "&".join(query_components)

    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobList)


def get_job_results(config: ClientConfig, job_id: str) -> api_pb.JobResult:
    """
    Get job results, if available.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID as integer.

    Results
    -------
    res_pb : ProfileJobResult
        Result is returned as a protobuf object. Or None if results are not available.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)
    url = utils.api_url(config, "jobs", job_id, "result")
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.JobResult, obj_id=job_id)


def get_profile_job_vizgraph(config: ClientConfig, job_id: str) -> api_pb.VizGraph:
    """
    Get profile job vizgraph, if available.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Profile job ID.

    Results
    -------
    vizgraph_pb : VizGraph
        Visualization graph representing the job.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)
    url = utils.api_url(config, "jobs", job_id, "profile", "vizgraph")
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.VizGraph, obj_id=job_id)


# Workaround for mypy having trouble with globals https://github.com/python/mypy/issues/5732
last: int


def _upload_asset(
    upload_url: str,
    path: str | Path,
    file_field_name: str,
    fields: Dict[str, Any] = {},
    verbose: bool = True,
    progress_bar_description: Optional[str] = None,
) -> None:
    """
    Helper upload function for models, datasets, etc.
    """
    path = os.path.expanduser(path)  # Expand home directory prefix.

    try:
        total_size = os.path.getsize(path)
    except FileNotFoundError:
        raise

    global last
    last = 0
    if verbose:
        tqdm_context = tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            colour="magenta",
            desc=progress_bar_description,
        )

        def update_progress(monitor):
            global last
            # Your callback function
            tqdm_context.update(monitor.bytes_read - last)
            last = monitor.bytes_read

    else:

        def update_progress(monitor):
            pass

    # We must manually edit the upload URL to follow redirects. The upload fails
    # if we allow python requests to auto-redirect during the multipart upload,
    # because requests will change all redirects to GET requests
    # (https://github.com/psf/requests/issues/1325)
    #
    #
    # Therefore, there are two potential paths here:
    # - the requests library will follow redirect responses until it gets a non-redirect response
    # - immediately get some non-redirect response back
    #
    # In either case, the non-redirect response we recieve doesn't matter; it's thrown away.
    # response.url will be populated with the last URL the requests package tried.
    # This will be the redirected URL if applicable, or the original URL if there was no redirect.
    #
    with open(path, "rb") as asset_file:
        fields[file_field_name] = ("model", asset_file, "application/octet-stream")
        num_redirects = 0
        while True:
            asset_file.seek(0)
            mpe = MultipartEncoder(fields=fields)
            mpm = MultipartEncoderMonitor(mpe, update_progress)
            headers = {"content-type": mpm.content_type}

            response = requests.post(
                upload_url, allow_redirects=False, data=mpm, headers=headers
            )
            if (
                response.status_code
                in [
                    requests.codes.moved,
                    requests.codes.found,
                    requests.codes.temporary_redirect,
                    requests.codes.permanent_redirect,
                ]
                and num_redirects < 5
            ):
                num_redirects += 1
                upload_url = response.headers["Location"]
            else:
                break

    if not api_status_codes.is_success(response.status_code):
        raise APIException(f"Failed to upload the file. Detail: {response.reason}")

    update_progress(SimpleNamespace(bytes_read=total_size))


def _create_model(
    config: ClientConfig,
    name: str,
    model_type: "api_pb.ModelType.ValueType",
    verbose: bool = True,
) -> api_pb.CreateUpdateResponse:
    """
    Create a model object.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Name of the model. If None, uses basename of path.
    model_type : api_pb.ModelType
        Type of the model.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    model_pb = api_pb.Model(name=name, model_type=model_type)
    url = utils.api_url(config, "models")
    return utils.response_as_protobuf(
        requests.post(url, data=model_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )


def _get_model_upload_url(
    config: ClientConfig, model_id: str, verbose: bool = True
) -> api_pb.FileUploadURL:
    """
    Get the URL with which the user should upload the model file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        ID of the model to query.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : FileUploadURL
        Returns a FileUploadURL protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    url = utils.api_url(config, f"models/{model_id}/upload_url")
    return utils.response_as_protobuf(
        requests.get(url, headers=header),
        api_pb.FileUploadURL,
    )


def _confirm_model_upload(
    config: ClientConfig, model_id: str, verbose: bool = True
) -> api_pb.CreateUpdateResponse:
    """
    Confirm to hub that the upload for the corresponding model is complete.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        ID of the model to update.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    model_pb = api_pb.Model(file_upload_complete=True)
    url = utils.api_url(config, f"models/{model_id}")
    return utils.response_as_protobuf(
        requests.patch(url, data=model_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )


def create_and_upload_model(
    config: ClientConfig,
    path: str,
    model_type,
    name: Optional[str] = None,
    verbose: bool = True,
) -> api_pb.CreateUpdateResponse:
    """
    Create a model object and upload the corresponding model file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    path : str or Path
        Local path to the model file.
    name : str
        Name of the model. If None, uses basename of path.
    model_type : api_pb.ModelType
        Type of the model.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    if not name:
        name = os.path.basename(path)

    # Create the model object
    cup_create_model = _create_model(config, name, model_type, verbose)
    if not cup_create_model.id or cup_create_model.status:
        return cup_create_model
    model_id = cup_create_model.id

    # Get model upload URL
    model_url = _get_model_upload_url(config, model_id, verbose)

    # Convert proto fields to a python dict.
    fields = {}
    for k, v in model_url.fields.items():
        fields[k] = v

    # Upload the model asset file
    _upload_asset(
        upload_url=model_url.url,
        path=path,
        file_field_name=model_url.file_field_name,
        fields=fields,
        verbose=verbose,
        progress_bar_description="Uploading model",
    )

    # Tell Hub that the model upload is done.
    upload_pb = _confirm_model_upload(config, model_id, verbose)
    cup_create_model.id = upload_pb.id
    return cup_create_model


def _create_dataset(
    config: ClientConfig, name: str, verbose: bool = True
) -> api_pb.CreateUpdateResponse:
    """
    Create a dataset object.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    name : str
        Name of the dataset.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    dataset_pb = api_pb.Dataset(name=name)
    url = utils.api_url(config, "datasets")
    return utils.response_as_protobuf(
        requests.post(url, data=dataset_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )


def _get_dataset_upload_url(
    config: ClientConfig, dataset_id: str, verbose: bool = True
) -> api_pb.FileUploadURL:
    """
    Get the URL with which the user should upload the dataset file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        ID of the dataset to query.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : FileUploadURL
        Returns a FileUploadURL protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    url = utils.api_url(config, f"datasets/{dataset_id}/upload_url")
    return utils.response_as_protobuf(
        requests.get(url, headers=header),
        api_pb.FileUploadURL,
    )


def _confirm_dataset_upload(
    config: ClientConfig, dataset_id: str, verbose: bool = True
) -> api_pb.CreateUpdateResponse:
    """
    Confirm to hub that the upload for the corresponding dataset is complete.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        ID of the dataset to query.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    header = utils.auth_header(config)

    dataset_pb = api_pb.Dataset(file_upload_complete=True)
    url = utils.api_url(config, f"datasets/{dataset_id}")
    return utils.response_as_protobuf(
        requests.patch(url, data=dataset_pb.SerializeToString(), headers=header),
        api_pb.CreateUpdateResponse,
    )


def create_and_upload_dataset(
    config: ClientConfig,
    path: str | Path,
    name: str,
    verbose: bool = True,
) -> api_pb.CreateUpdateResponse:
    """
    Create dataset and upload the corresponding h5 file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    path : str or Path
        Local path to the model file.
    name : Optional[str]
        Name of the model.
    verbose : bool
        If true, will show progress bar in standard output.

    Returns
    -------
    res_pb : CreateUpdateResponse
        Returns a CreateUpdateResponse protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """

    # Create the dataset object
    cup_create_dataset = _create_dataset(config, name, verbose)
    if not cup_create_dataset.id or cup_create_dataset.status:
        return cup_create_dataset
    dataset_id = cup_create_dataset.id

    # Get dataset upload URL
    dataset_url = _get_dataset_upload_url(config, dataset_id, verbose)

    # Convert proto fields to a python dict.
    fields = {}
    for k, v in dataset_url.fields.items():
        fields[k] = v

    # Upload the dataset asset file
    _upload_asset(
        upload_url=dataset_url.url,
        path=path,
        file_field_name=dataset_url.file_field_name,
        fields=fields,
        verbose=verbose,
        progress_bar_description="Uploading dataset",
    )

    # Tell Hub that the dataset upload is done.
    upload_pb = _confirm_dataset_upload(config, dataset_id, verbose)
    cup_create_dataset.id = upload_pb.id
    return cup_create_dataset


def get_dataset(config: ClientConfig, dataset_id: str) -> api_pb.Dataset:
    """
    Get info about an uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.

    Returns
    -------
    dataset_pb : Dataset
        Dataset info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets", dataset_id)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Dataset, obj_id=dataset_id)


def get_dataset_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.DatasetList:
    """
    Get list of datasets visible to the authenticated user.


    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int | None
        Limit query response size.

    Returns
    -------
    list_pb : DatasetList
        Dataset list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.DatasetList)


def get_model(config: ClientConfig, model_id: str) -> api_pb.Model:
    """
    Get info about an uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.

    Returns
    -------
    model_pb : Model
        Model info as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models", model_id)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.Model, obj_id=model_id)


def get_model_list(
    config: ClientConfig, offset: int = 0, limit: int | None = None
) -> api_pb.ModelList:
    """
    Get list of models visible to the authenticated user.


    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    offset : int
        Offset the query.
    limit : int
        Limit query response size.

    Returns
    -------
    list_pb : ModelList
        Model list as protobuf object.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models")
    url += utils.prepare_offset_limit_query(offset, limit)
    header = utils.auth_header(config)
    response = requests.get(url, headers=header)
    return utils.response_as_protobuf(response, api_pb.ModelList)


def download_model_info(config: ClientConfig, model_id: str) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "models", model_id, "download")
    header = utils.auth_header(config)
    return utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )


def download_model(
    config: ClientConfig,
    model_id: str,
    file_path: str,
    verbose: bool = True,
    extract_model: bool = False,
) -> str:
    """
    Download a previously uploaded model.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    model_id : str
        Model ID.
    file_path : str
        file location to store model to

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_model_info(config, model_id)
    return utils.download_file(
        response.url, response.filename, file_path, verbose, extract_model
    )


def download_compiled_model(
    config: ClientConfig, job_id: str, file_path: str, verbose: bool = True
) -> str:
    """
    Download compiled model to file.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    job_id : str
        Job ID.
    file_path : str
        file location to store compiled model to

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    # fetch compiled model
    url = utils.api_url(config, "jobs", job_id, "download_compiled_model")
    header = utils.auth_header(config)
    response = utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )
    return utils.download_file(response.url, response.filename, file_path, verbose)


__all__ = [
    "utils",
    "APIException",
    "ClientConfig",
    "Shapes",
    "get_auth_user",
    "get_user",
    "get_user_list",
    "get_dataset",
    "get_dataset_list",
    "get_device_list",
    "create_profile_job",
    "get_job",
    "get_job_list",
    "get_job_results",
    "get_profile_job_vizgraph",
    "create_validation_job",
    "create_and_upload_dataset",
    "create_and_upload_model",
    "download_model",
    "download_compiled_model",
    "get_model",
    "get_model_list",
]


def download_dataset_info(
    config: ClientConfig, dataset_id: str
) -> api_pb.FileDownloadURL:
    """
    Get download information for a previously uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.

    Returns
    -------
    response : api_pb.FileDownloadURL
        Download information.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    url = utils.api_url(config, "datasets", dataset_id, "download_data")
    header = utils.auth_header(config)
    return utils.response_as_protobuf(
        requests.get(url, headers=header), api_pb.FileDownloadURL
    )


def download_dataset(
    config: ClientConfig, dataset_id: str, file_path: str, verbose: bool = True
) -> str:
    """
    Download a previously uploaded dataset.

    Parameters
    ----------
    config : ClientConfig
        API authentication configuration.
    dataset_id : str
        Dataset ID.
    file_path : str
        file location to store model to

    Returns
    -------
    file_path : str
        Path to the saved file.

    Raises
    ------
    APIException
        Raised if request has failed.
    """
    response = download_dataset_info(config, dataset_id)
    return utils.download_file(response.url, response.filename, file_path, verbose)
