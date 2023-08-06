from __future__ import annotations

import json
import os
import sys
import posixpath
import tempfile
import textwrap
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional, OrderedDict, Tuple, Union, cast
from urllib.parse import urljoin
from zipfile import ZipFile

import deprecation  # type: ignore
import h5py
import numpy as np
from pkg_resources import parse_version as pv  # type: ignore

from . import api_status_codes
from . import public_api_pb2 as api_pb
from . import public_rest_api as api
from .public_rest_api import APIException, ClientConfig, DatasetEntries, Shapes
from .util.dataset_entries_converters import (
    dataset_entries_to_h5,
    h5_to_dataset_entries,
)

MISSING_METRIC_VALUE = None

IS_WINDOWS = sys.platform in ["win32", "msys", "cygwin"]

ESPRESSO_NET_FILE = "model.espresso.net"


def _profile_pb_to_python_dict(profile_pb: api_pb.ProfileDetail) -> dict:
    layer_details = []
    for layer_detail_pb in profile_pb.layer_details:
        layer_details.append(
            {
                "name": layer_detail_pb.name,
                "type": layer_detail_pb.layer_type_name,
                # Remove the compute unit enum prefix (COMPUTE_UNIT_).
                "compute_unit": api_pb.ComputeUnit.Name(layer_detail_pb.compute_unit)[
                    len("COMPUTE_UNIT_") :
                ],
            }
        )

    execution_summary: Dict[str, int | Tuple[int, int] | None] = {}

    if profile_pb.major_version == 1:
        execution_summary = {
            "estimated_inference_time": profile_pb.execution_time,
            "estimated_inference_peak_memory": profile_pb.after_execution_peak_memory,
            "first_load_time": profile_pb.cold_load_time,
            "first_load_peak_memory": profile_pb.after_cold_load_peak_memory,
            "warm_load_time": profile_pb.warm_load_time,
            "warm_load_peak_memory": profile_pb.after_warm_load_peak_memory,
            "compile_time": profile_pb.compile_time,
            "compile_peak_memory": profile_pb.after_compile_peak_memory,
        }

        if profile_pb.minor_version >= 1:
            stage_memories: List[Tuple[str, api_pb.ProfileDetail.MemoryUsage]] = [
                ("compile", profile_pb.compile_memory),
                ("first_load", profile_pb.cold_load_memory),
                ("warm_load", profile_pb.warm_load_memory),
                ("inference", profile_pb.execution_memory),
            ]
            for stage, memory in stage_memories:
                # ByteSize() > 0 means the field was explicitly set
                if memory.ByteSize() > 0:
                    increase = memory.increase
                    peak = memory.peak
                    execution_summary[f"{stage}_memory_increase_range"] = (
                        increase.lower,
                        increase.upper,
                    )
                    execution_summary[f"{stage}_memory_peak_range"] = (
                        peak.lower,
                        peak.upper,
                    )
                else:
                    execution_summary[
                        f"{stage}_memory_increase_range"
                    ] = MISSING_METRIC_VALUE
                    execution_summary[
                        f"{stage}_memory_peak_range"
                    ] = MISSING_METRIC_VALUE

    else:
        execution_summary = {
            "estimated_inference_time": profile_pb.execution_time,
            "estimated_inference_peak_memory": MISSING_METRIC_VALUE,
            "first_load_time": profile_pb.load_time,
            "first_load_peak_memory": MISSING_METRIC_VALUE,
            "warm_load_time": MISSING_METRIC_VALUE,
            "warm_load_peak_memory": MISSING_METRIC_VALUE,
            "compile_time": MISSING_METRIC_VALUE,
            "compile_peak_memory": profile_pb.peak_memory_usage,
            "compile_memory_increase_range": MISSING_METRIC_VALUE,
            "compile_memory_peak_range": MISSING_METRIC_VALUE,
            "first_load_memory_increase_range": MISSING_METRIC_VALUE,
            "first_load_memory_peak_range": MISSING_METRIC_VALUE,
            "warm_load_memory_increase_range": MISSING_METRIC_VALUE,
            "warm_load_memory_peak_range": MISSING_METRIC_VALUE,
            "inference_load_memory_increase_range": MISSING_METRIC_VALUE,
            "inference_load_memory_peak_range": MISSING_METRIC_VALUE,
        }

    return {
        "execution_summary": execution_summary,
        "execution_detail": layer_details,
    }


def _class_repr_print(obj, fields) -> str:
    """
    Display a class repr according to some simple rules.

    Parameters
    ----------
    obj: Object to display a repr for
    fields: List of Union[str | (str, str)]
    """

    # Record the max_width so that if width is not provided, we calculate it.
    max_width = len("Class")

    # Add in the section header.
    section_title = obj.__class__.__name__
    out_fields = [section_title, "-" * len(section_title)]

    # Add in all the key-value pairs
    for f in fields:
        if type(f) == tuple:
            out_fields.append(f)
            max_width = max(max_width, len(f[0]))
        else:
            out_fields.append((f, getattr(obj, f)))
            max_width = max(max_width, len(f))

    # Add in the empty footer.
    out_fields.append("")

    # Now, go through and format the key_value pairs nicely.
    def format_key_pair(key, value) -> str:
        return key.ljust(max_width, " ") + " : " + str(value)

    out_fields = [s if type(s) == str else format_key_pair(*s) for s in out_fields]
    return "\n".join(out_fields)


def _get_source_model_type_from_model_type(model_type: api_pb.ModelType.ValueType):
    if model_type not in api_pb.ModelType.values():
        model_type = api_pb.ModelType.MODEL_TYPE_UNSPECIFIED
    return SourceModelType(model_type)


def _is_in_zip(zip: ZipFile, filename: str) -> bool:
    return filename in zip.namelist()


def _is_valid_zipped_mlmodelc(filepath: str) -> bool:
    with ZipFile(filepath, "r") as zippedModel:
        # Expecting model.espresso.net at the root level
        #  1. <filepath>/model.espresso.net or
        #  2. <filepath>/model0/model.espresso.net in case of pipeline model
        return _is_in_zip(zippedModel, ESPRESSO_NET_FILE) or _is_in_zip(
            zippedModel, os.path.join(filepath, "model0", ESPRESSO_NET_FILE)
        )


## ERROR HANDLING ##
class Error(Exception):
    """
    Base class for all exceptions explicitly thrown by the API.

    Other exception may be raised from dependent third party packages.
    """

    def __init__(self, message):
        super().__init__(message)


class InternalError(Error):
    """
    Internal API failure; please contact support@tetra.ai for assistance.
    """

    def __init__(self, message):
        super().__init__(message)


class UserError(Error):
    """
    Something in the user input caused a failure; you may need to adjust your input.
    """

    def __init__(self, message):
        super().__init__(message)


def _visible_textbox(text: str) -> str:
    """
    Letting exceptions terminate a python program is a cluttered way to give
    user feedback. This box is to draw attention to action items for users.
    """
    width = 70
    text = textwrap.dedent(text).strip()
    wrapper = textwrap.TextWrapper(width=width - 4)
    header = "┌" + "─" * (width - 2) + "┐\n"
    footer = "\n└" + "─" * (width - 2) + "┘"

    lines = ["| " + line.ljust(width - 4) + " |" for line in wrapper.wrap(text)]
    return header + "\n".join(lines) + footer


def _api_call(api_func, *args, **kwargs) -> Any:
    """
    Wrapper to re-raise the most common API exceptions appriopriate for the
    client.
    """
    try:
        return api_func(*args, **kwargs)
    except api.APIException as e:
        config_path = api.get_config_path(expanduser=False)
        if e.status_code == api_status_codes.HTTP_404_NOT_FOUND:
            raise UserError(str(e))
        elif e.status_code == api_status_codes.HTTP_401_UNAUTHORIZED:
            long_message = _visible_textbox(
                "Failure to authenticate is likely caused by a bad or outdated API "
                f"token in your {config_path} file. Please go to your Account page "
                "to view your current token."
            )

            raise UserError(f"Failed to authenticate.\n{long_message}")
        elif e.status_code == api_status_codes.API_CONFIGURATION_MISSING_FIELDS:
            long_message = _visible_textbox(
                f"Your {config_path} file is missing required fields. "
                "Please go to your Account page to see an example."
            )

            raise UserError(f"Failed to load configuration file.\n{long_message}")
        elif e.status_code == api_status_codes.HTTP_500_INTERNAL_SERVER_ERROR:
            long_message = _visible_textbox(
                "The error suggests that Tetra Hub is experiencing a service failure. "
                "Please contact support at support@tetra.ai."
            )

            raise InternalError(f"Internal API failure.\n{long_message}")
        else:
            # Re-raise, let the function catch it, or let it bubble up
            raise


## DATASET ##


class Dataset:
    """

    A dataset should not be constructed directly. It is constructed by the hub client
    through :py:func:`tetra_hub.upload_dataset`,  :py:func:`tetra_hub.get_dataset` or :py:func:`tetra_hub.get_datasets`.

    Attributes
    ----------
    dataset_id : str
        The dataset ID.
    creation_time : datetime
        The time this dataset was created.
    dataset_name : str
        Name of this dataset
    expiration_time: datetime
        The time this dataset will expire.
    """

    def __init__(
        self,
        owner: Client,
        dataset_id: str,
        creation_time: datetime,
        expiration_time: datetime,
        dataset_name: str,
        verbose: bool,
        data: Optional[DatasetEntries] = None,
    ):
        self._owner = owner
        self.name = dataset_name
        self.dataset_id = dataset_id
        self.creation_time = creation_time
        self.expiration_time = expiration_time
        self.verbose = verbose
        self._data = data

    def download(self, filename: Optional[str] = None) -> Union[DatasetEntries, str]:
        """
        Downloads the dataset entries either to memory or to an h5py (.h5) file.

        Parameters
        ----------
        filename : Optional[str]
            If filename is specified the dataset is downloaded to file, otherwise to memory.

        Returns
        -------
        : OrderedDict[str, List[np.ndarray]] | OrderedDict[str, np.ndarray] | Dict[str, List[np.ndarray]] | Dict[str, np.ndarray] | str
            Loaded data instance or file name.
        """
        if self._data is None:
            if filename is not None:
                download_file = filename
            else:
                # delete=False to be compatible with Windows
                with tempfile.NamedTemporaryFile(delete=False) as file:
                    download_file = file.name
                # Close the file to avoid double-open on Windows

            download_file = _api_call(
                api.download_dataset,
                self._owner.config,
                self.dataset_id,
                file_path=download_file,
                verbose=self.verbose,
            )
            if filename is not None:
                return download_file

            with h5py.File(download_file, "r") as h5f:
                self._data = h5_to_dataset_entries(h5f)

            os.remove(download_file)

            return self._data
        else:
            if filename is None:
                return self._data

            if os.path.isdir(filename):
                # Grab filename from the API and append it to the path.
                dataset_info = _api_call(
                    api.download_dataset_info, self._owner.config, self.dataset_id
                )
                filename = os.path.join(filename, dataset_info.filename)

                # Append suffix if necessary, so we don't overwrite.
                filename, _ = api.utils.get_unique_path(filename)

            with h5py.File(filename, "w") as h5f:
                dataset_entries_to_h5(self._data, h5f)

            assert isinstance(filename, str)
            return filename

    def __str__(self) -> str:
        return f"Dataset(id='{self.dataset_id}', name='{self.name}', expiration_time='{self.expiration_time}')"

    def get_expiration_status(self) -> str:
        if datetime.now() > self.expiration_time:
            return "Expired"
        else:
            return "Not Expired"

    def __repr__(self) -> str:
        return _class_repr_print(
            self,
            [
                "dataset_id",
                "name",
                "creation_time",
                ("expiration_status", self.get_expiration_status()),
            ],
        )


## DEVICES ##


@dataclass
class Device:
    """
    Create a target device representation.

    The actual target device selection is done when a job is submitted.

    Attributes
    ----------
    name:str
        A name must be an exact match with an existing device, e.g. `"Apple iPhone 13"`.
    os:str
        The OS can either be empty, a specific version, or a version interval. If a
        specific vesion is specified (`"15.2"`), it must be an exact match with an
        existing device.  An interval can be used to get a range of OS
        versions. The OS interval must be a
        `right-open mixed interval <https://simple.wikipedia.org/wiki/Interval_(mathematics)#Mixed_Intervals>`_.
        Either side of an interval can be empty, e.g. `"[14,15)"` or `"[15,)"`.
        If the OS is empty, this device represents the device with the latest OS version
        selected from all devices compatible with the name and attriutes.
    attributes: str|List[str]
        Additional device attributes. The selected device is compatible with all
        attributes specified. The supported attributes are:

            * ``"vendor:apple"``

            * ``"framework:coreml"``

            * ``"os:ios"``

            * ``"chipset:apple-a11"``

            * ``"chipset:apple-a12"``

            * ``"chipset:apple-a12z"``

            * ``"chipset:apple-a13"``

            * ``"chipset:apple-a14"``

            * ``"chipset:apple-a15"``

            * ``"chipset:apple-m1"``

    Examples
    --------
    ::

        import tetra_hub as hub

    Select a target device for iPhone 12 with specifically iOS 14.8::

        device = hub.Device("Apple iPhone 12", "14.8")

    Select a target device with OS major version 15::

        device = hub.Device(os="[15,16)")

    Select a target device with an A15 chipset::

        device = hub.Device(attributes="chipset:apple-a15")

    Fetch a list of devices using :py:func:`~tetra_hub.get_devices`::

        devices = hub.get_devices()
    """

    name: str = ""
    os: str = ""
    attributes: Union[str, List[str]] = cast(
        Union[str, List[str]], field(default_factory=list)
    )


## MODELS ##

SourceModel = Union[
    "torch.jit.TopLevelTracedModule",  # type: ignore # noqa: F821 (imported conditionally)
    "coremltools.models.model.MLModel",  # type: ignore # noqa: F821 (imported conditionally)
    bytes,
]

TargetModel = Union[
    "coremltools.models.model.MLModel",  # type: ignore # noqa: F821 (imported conditionally)
    bytes,
]


class SourceModelType(Enum):
    """
    Set of supported input model types.
    """

    UNRECOGNIZED_MODEL_TYPE = api_pb.ModelType.MODEL_TYPE_UNSPECIFIED
    TORCHSCRIPT = api_pb.ModelType.MODEL_TYPE_TORCHSCRIPT
    MLMODEL = api_pb.ModelType.MODEL_TYPE_MLMODEL
    TFLITE = api_pb.ModelType.MODEL_TYPE_TFLITE
    MLMODELC = api_pb.ModelType.MODEL_TYPE_MLMODELC


class Model:
    """
    Neural network model object.

    A model should not be constructed directly. It is constructed by the hub client
    through :py:func:`tetra_hub.upload_model`, :py:func:`tetra_hub.get_model`, or
    :py:func:`tetra_hub.get_models`.

    Attributes
    ----------
    model_id : str
        The model ID.
    date : datetime
        The time this model was uploaded.
    model_type : SourceModelType
        The type of the model.
    name : str
        An optional user-provided name to identify the model.
    """

    def __init__(
        self,
        owner: Client,
        model_id: str,
        date: datetime,
        model_type: SourceModelType,
        name: str,
        model: Optional[Any],  # Any instead of SourceModel to keep mypy happy
        verbose: bool,
    ):
        self._owner = owner
        self.model_id = model_id
        self.date = date
        self.model_type = model_type
        self.name = name
        self._model = model  # access through download
        self.verbose = verbose

    def download(self, filename: Optional[str] = None) -> Union[SourceModel, str]:
        """
        Downloads source model either to memory or to file.

        Parameters
        ----------
        filename : Optional[str]
            If filename is specified the model is downloaded to file, otherwise to memory.

        Returns
        -------
        : SourceModel | str
            Loaded model instance or file name. The returned type depends on the model type.
        """
        if self._model is None:
            if filename is not None:
                download_file = filename
            else:
                if self.model_type == SourceModelType.UNRECOGNIZED_MODEL_TYPE:
                    raise UserError(
                        "Model not recognized."
                        " Please upgrade tetra-hub client to be able to download the model."
                    )
                elif IS_WINDOWS and self.model_type == SourceModelType.MLMODEL:
                    raise UserError(
                        "Cannot load a Core ML model in memory on Windows "
                        "platform. Specify `filename` to download to disk."
                    )
                elif self.model_type == SourceModelType.MLMODELC:
                    raise UserError(
                        "Cannot load a compiled Core ML (.mlmodelc) into memory. "
                        "Please specify a filename to download it to disk without loading it."
                    )

                # delete=False to be compatible with Windows
                with tempfile.NamedTemporaryFile(delete=False) as file:
                    download_file = file.name
                # Close the file to avoid double-open on Windows

            download_file = _api_call(
                api.download_model,
                self._owner.config,
                self.model_id,
                file_path=download_file,
                verbose=self.verbose,
            )
            if filename is not None:
                return download_file

            elif self.model_type == SourceModelType.TORCHSCRIPT:
                import torch

                self._model = torch.jit.load(download_file)
            elif self.model_type == SourceModelType.MLMODEL:
                import coremltools

                self._model = coremltools.models.MLModel(download_file)
            elif self.model_type == SourceModelType.TFLITE:
                with open(download_file, "rb") as tf_file:
                    self._model = tf_file.read()

            os.remove(download_file)

            return self._model
        else:
            if filename is None:
                return self._model

            if os.path.isdir(filename):
                # Grab filename from the API and append it to the path.
                model_info = _api_call(
                    api.download_model_info, self._owner.config, self.model_id
                )
                filename = os.path.join(filename, model_info.filename)

                # Append suffix if necessary, so we don't overwrite.
                filename, _ = api.utils.get_unique_path(filename)

            if self.model_type == SourceModelType.TORCHSCRIPT:
                import torch

                torch.jit.save(self._model, filename)
            elif self.model_type == SourceModelType.MLMODEL:
                import coremltools

                self._model.save(filename)
            elif self.model_type == SourceModelType.TFLITE:
                assert filename is not None and isinstance(self._model, bytes)
                with open(filename, "wb") as tffile:
                    tffile.write(self._model)

            return filename

    @deprecation.deprecated(
        deprecated_in="0.3.0", details="Please use the 'download' API instead."
    )
    def download_model(self, filename: Optional[str] = None) -> Union[SourceModel, str]:
        return self.download(filename)

    def __str__(self) -> str:
        return f"Model(model_id='{self.model_id}', name='{self.name}')"

    def __repr__(self) -> str:
        return _class_repr_print(
            self, ["model_id", "name", ("model_type", self.model_type.name), "date"]
        )


def _determine_model_type(model: Union[Model, SourceModel, str]) -> SourceModelType:
    if isinstance(model, Model):
        return model.model_type
    elif isinstance(model, str):
        _, suffix = os.path.splitext(model)
        if suffix == ".pt" or suffix == ".pth":
            return SourceModelType.TORCHSCRIPT
        elif suffix == ".mlmodel":
            return SourceModelType.MLMODEL
        elif suffix == ".tflite":
            return SourceModelType.TFLITE
        elif model.endswith(".mlmodelc.zip"):
            return SourceModelType.MLMODELC
        else:
            if suffix == "":
                raise UserError(
                    rf"""Path "{model}" is a directory or has no extension, which is not supported. Following model types are supported:
                            * TorchScript : model path must have extension .pt or .pth"
                            * Core ML Model : model path must have extension .mlmodel
                            * Compiled Core ML Model : model path must have extension .mlmodelc.zip"""
                )
            raise UserError(
                rf"""Extension {suffix} is not supported. Following model types are supported:
                        * TorchScript : model path must have extension .pt or .pth
                        * Core ML Model : model path must have extension .mlmodel
                        * Compiled Core ML Model : model path must have extension .mlmodelc.zip"""
            )
    elif type(model).__name__ in {"TopLevelTracedModule", "RecursiveScriptModule"}:
        return SourceModelType.TORCHSCRIPT
    elif type(model).__name__ == "MLModel":
        return SourceModelType.MLMODEL
    elif isinstance(model, bytes) and model[4:8] == b"TFL3":
        return SourceModelType.TFLITE
    else:
        module_name_list = [model_type.__module__ for model_type in type(model).mro()]
        if "torch.nn.modules.module" in module_name_list:
            raise UserError("The torch model must be traced.")
        raise UserError(
            r"""Unsupported model type. The supported model types are:
                    * Traced TorchScript model
                    * Core ML model """
        )


def _determine_model_extension(type: SourceModelType) -> str:
    if type == SourceModelType.TORCHSCRIPT:
        suffix = ".pt"
    elif type == SourceModelType.MLMODEL:
        suffix = ".mlmodel"
    elif type == SourceModelType.TFLITE:
        suffix = ".tflite"
    elif type == SourceModelType.MLMODELC:
        suffix = ".mlmodelc.zip"
    return suffix


## JOBS ##


@dataclass
class JobStatus:
    """
    Status of a job.

    Attributes
    ----------
    code: str
        Status code for the job. Valid codes are "SUCCESS", "FAILED", "UNKNOWN",
        OPTIMIZING_MODEL", "PROVISIONING_DEVICE", and "MEASURING_PERFORMANCE"
    message: str
        Optional error message.
    """

    class State(Enum):
        SUCCESS = api_pb.JobState.JOB_STATE_DONE
        FAILED = api_pb.JobState.JOB_STATE_FAILED
        UNSPECIFIED = api_pb.JobState.JOB_STATE_UNSPECIFIED
        OPTIMIZING_MODEL = api_pb.JobState.JOB_STATE_OPTIMIZING_MODEL
        PROVISIONING_DEVICE = api_pb.JobState.JOB_STATE_PROVISIONING_DEVICE
        MEASURING_PERFORMANCE = api_pb.JobState.JOB_STATE_MEASURING_PERFORMANCE
        VALIDATING_MODEL = api_pb.JobState.JOB_STATE_VALIDATING_MODEL

    _len_largest_state: ClassVar[int] = max([len(enum_val.name) for enum_val in State])

    state: State
    message: Optional[str] = None

    @property
    def code(self) -> str:
        return self.state.name

    @property
    def symbol(self) -> str:
        if self.failure:
            return "❌"
        elif self.success:
            return "✅"
        elif self.state == JobStatus.State.UNSPECIFIED:
            return ""
        else:
            return "⏳"

    @property
    def success(self) -> bool:
        """
        Returns whether a job finished succesfully.

        Returns
        -------
        : bool
            returns true if the job finished succesfully.
        """
        return self.state == JobStatus.State.SUCCESS

    @property
    def failure(self) -> bool:
        """
        Returns whether a job failed.

        Returns
        -------
        : bool
            returns true if the job failed.
        """
        return self.state == JobStatus.State.FAILED

    @property
    def finished(self) -> bool:
        """
        Returns whether a job finished.

        Returns
        -------
        : bool
            returns true if the job finished.
        """
        return self.success or self.failure

    @property
    def running(self) -> bool:
        """
        Returns whether a job is still riunning.

        Returns
        -------
        : bool
            returns true if the job is still running.
        """
        return not self.finished

    def __eq__(self, obj) -> bool:
        if isinstance(obj, JobStatus.State):
            return self.state == obj
        elif isinstance(obj, str):
            return self.code == obj
        return self.state == obj.state and self.message == obj.message

    def __repr__(self) -> str:
        return _class_repr_print(self, ["code", "message"])


@dataclass
class JobResult:
    """
    Job result structure.

    Attributes
    ----------
    status : JobStatus
        Status of the job.
    url: str
        The url for the job.
    artifacts_dir:str
        Directory where the results are stored.
    """

    status: JobStatus
    url: Optional[str]
    artifacts_dir: str


@dataclass
class ValidationJobResult(JobResult):
    # TODO: Have the output below be produced by doctest
    """
    Validation Job result structure.

    Examples
    --------
    Fetch a job result::

        import tetra_hub as hub
        job = hub.get_jobs()[0]
        job_result = job.download_results("artifacts")

    """

    def __repr__(self) -> str:
        # Successful job
        if self.status.success:

            return _class_repr_print(self, ["status", "artifacts_dir"])
        else:
            # Failed job
            return _class_repr_print(self, ["status"])


@dataclass
class ProfileJobResult(JobResult):
    # TODO: Have the output below be produced by doctest
    """
    Profile Job result structure.

    Attributes
    ----------
    profile : Dict
        The profile result as a python dictionary for a successful job.

    Examples
    --------
    Fetch a job result::

        import tetra_hub as hub
        job = hub.get_jobs()[0]
        job_result = job.download_results("artifacts")

    Print the profiling results as a dictionary structure::

        profile = job_result.download_profile()

    Print the model runtime latency in milliseconds::

        latency_ms = job_result.profile["execution_summary"]["execution_time"] / 1000
    """

    profile: Dict

    @property
    def _compute_unit_breakdown(self) -> OrderedDict[str, int]:
        breakdown: OrderedDict[str, int] = OrderedDict(
            [("NPU", 0), ("GPU", 0), ("CPU", 0)]
        )
        for layer_detail in self.profile["execution_detail"]:
            breakdown[layer_detail["compute_unit"]] += 1
        return breakdown

    def __repr__(self) -> str:
        # Successful job
        if self.status.success:
            profile_sum = self.profile["execution_summary"]
            breakdown = self._compute_unit_breakdown
            breakdown_str = ", ".join(
                f"{k}: {v}" for k, v in breakdown.items() if v > 0
            )
            return _class_repr_print(
                self,
                [
                    "status",
                    "url",
                    "artifacts_dir",
                    (
                        "Estimated Inference Time (ms)",
                        profile_sum["estimated_inference_time"] / 1000,
                    ),
                    ("Load Time (ms)", profile_sum["warm_load_time"] / 1000),
                    (
                        "Peak Memory (MB)",
                        profile_sum["estimated_inference_peak_memory"] / 1024 / 1024,
                    ),
                    ("Compute Units (layers)", breakdown_str),
                ],
            )
        else:
            # Failed job
            return _class_repr_print(self, ["status", "url"])


class Job(ABC):
    """
    Job for a model and a device.

    A job should not be constructed directly. It is constructed by the hub client
    through :py:func:`tetra_hub.submit_profile_job`, :py:func:`tetra_hub.submit_validation_job`,
    :py:func:`tetra_hub.get_job`, or :py:func:`tetra_hub.get_jobs`.

    Attributes
    ----------
    job_id : str
        The job ID.
    device : Device
        The device for this job.
    model : Model
        The model for the job.
    name : str
        Name of this job
    date : datetime
        The time this job was submitted.
    options: str
        Options passed during the job submission.
    """

    _polling_interval: int = 10

    def __init__(
        self,
        owner: Client,
        job_id: str,
        device: Device,
        model: Model,
        name: str,
        date: datetime,
        options: str,
        verbose: bool,
        job_type: str,
        in_progress_states: List[JobStatus.State],
    ):
        self._owner = owner
        self._job_type = job_type
        self.job_id = job_id
        self.device = device
        self.model = model
        self.name = name
        self.date = date
        self.options = options
        self.verbose = verbose
        self._job_type_str = job_type
        self._in_progress_states = in_progress_states

    @property
    def url(self) -> str:
        """
        Returns the URL for the job.
        Returns
        -------
        : str
            The URL for the job.
        """

        return f"{self._owner._web_url_of_job(self.job_id)}"

    @property
    def job_type(self) -> str:
        return self._job_type

    def wait(self, timeout: Optional[int] = None) -> JobStatus:
        """
        Block until this job finishes.

        Parameters
        ----------
        timeout : Optional[int]
            If provided, a TimeoutError will be raised after waiting this many seconds.

            If `None`, this client will not time out the job, meaning it will block
            an indefinite amount of time waiting for the job to finish.

            HOWEVER, Tetra Hub will fail / time out any job a set amount of time
            after its creation. Therefore, even if `timeout` is `None`, the
            runtime of this method will still have a finite upper bound.

        Returns
        -------
        : str
            The final, "finished" (SUCCESS or FAILED) status for this job.

        Raises
        ------
        TimeoutError
            Raised only if a **client-side** timeout occurs, when param "timeout" != None.

            If the Tetra Hub server times out the job, this error will NOT be raised, and a
            FAILED job status will be returned instead.

        """

        def status_text(job_status: JobStatus) -> str:
            """
            Generates status text:
            [Status Symbol] [Status Name] [Progress Bar] [Progress Counter]
            """
            # Make sure we always output a string of the same size
            # by padding smaller status codes with spaces.
            status_code = job_status.code.ljust(JobStatus._len_largest_state)

            progress_bar: str
            progress_count: str
            if job_status.finished:
                # Don't show progress bar when we finish.
                # Pad with empty spaces to make sure we always
                # output the same string length.
                progress_count = "".ljust(3)
                progress_bar = progress_count
            else:
                # Determine number of done states to generate progress bar & count.
                total_states = len(self._in_progress_states)
                done_states = self._in_progress_states.index(job_status.state)

                progress_count = f"{str(done_states)}/{str(total_states)}"
                progress_bar = (
                    f"{'█' * done_states}{'░' * (total_states - done_states)}"
                )

            # Construct and return the status string.
            return f"{status.symbol} {status_code}{status.message or ''} {progress_bar} {progress_count}"

        def get_in_progress_dots(num_dots) -> Tuple[int, str]:
            """Generates a string of length 3 that contains num_dots periods."""
            num_dots = 0 if num_dots >= 3 else num_dots + 1
            return (num_dots, "." * num_dots + " " * (3 - num_dots))

        status = self.get_status()
        if not status.running:
            return status

        if self.verbose:
            print(
                f"Waiting for {self.job_type} job ({self.job_id}) completion. Type Ctrl+C to stop waiting at any time."
            )

        num_dots = 3
        time_elapsed = 0
        sleep_seconds = Job._polling_interval if not self.verbose else 1
        while status.running:
            if self.verbose:
                num_dots, dots_str = get_in_progress_dots(num_dots)
                print(f"    {status_text(status)} {dots_str}", end="\r")

            if timeout and time_elapsed >= timeout:
                raise TimeoutError(
                    f"Waiting for {self.job_type} job ({self.job_id}) completion timed out after {sleep_seconds} seconds."
                )

            time.sleep(sleep_seconds)
            time_elapsed += sleep_seconds

            if time_elapsed % Job._polling_interval == 0:
                status = self.get_status()

        if self.verbose:
            print(f"    {status_text(status)}    ", end="\a\n")

        return status

    def get_status(self) -> JobStatus:
        """
        Returns the status of a job.

        Returns
        -------
        : JobStatus
            The status of the job
        """
        job_pb = _api_call(api.get_job, self._owner.config, self.job_id)
        job_type = job_pb.WhichOneof("job")

        state: "api_pb.JobState.ValueType"
        failure_reason: str
        if job_type == "profile_job":
            state = job_pb.profile_job.job_state
            failure_reason = job_pb.profile_job.failure_reason
        elif job_type == "validation_job":
            state = job_pb.validation_job.job_state
            failure_reason = job_pb.validation_job.failure_reason
        else:
            raise NotImplementedError(f"Cannot fetch status for job of type {job_type}")

        return JobStatus(JobStatus.State(state), failure_reason)

    @abstractmethod
    def download_results(self, artifacts_dir: str) -> JobResult:
        raise NotImplementedError


class ProfileJob(Job):
    """
    Profiling job for a model, a set of input shapes, and a device.

    A profile job should not be constructed directly. It is constructed by the hub client
    through :py:func:`tetra_hub.submit_profile_job`, :py:func:`tetra_hub.get_job`, or
    :py:func:`tetra_hub.get_jobs`.

    Attributes
    ----------
    job_id : str
        The job ID.
    device : Device
        The device for this job.
    model : Model
        The model for the job.
    name : str
        Name of this job
    date : datetime
        The time this job was submitted.
    shapes : Shapes
        The input shapes for the model.
    options: str
        Options passed during the job submission.
    """

    __in_progress_states: ClassVar[List[JobStatus.State]] = [
        JobStatus.State.OPTIMIZING_MODEL,
        JobStatus.State.PROVISIONING_DEVICE,
        JobStatus.State.MEASURING_PERFORMANCE,
    ]
    __job_type_str = "profiling"

    def __init__(
        self,
        owner: Client,
        job_id: str,
        device: Device,
        model: Model,
        target_model: Optional[Model],
        name: str,
        date: datetime,
        options: str,
        verbose: bool,
        shapes: Shapes,
    ):
        super().__init__(
            owner=owner,
            job_id=job_id,
            device=device,
            model=model,
            name=name,
            date=date,
            options=options,
            verbose=verbose,
            job_type=self.__job_type_str,
            in_progress_states=self.__in_progress_states,
        )
        self.shapes: Shapes = shapes
        self._target_model = target_model

    def _write_profile(self, profile: Dict, dst_path: str) -> str:
        """
        Saves the profile json to disk.

        Parameters
        ----------
        dst_path :
            Dir or filename to save to.

        Returns
        -------
        : str
            The path of the saved profile json.
        """
        if os.path.isdir(dst_path):
            # Append a reasonable filename to save to.
            dst_path = os.path.join(dst_path, f"{self.name}_{self.job_id}_results.json")
            # Append suffix if destination file exists.
            dst_path, _ = api.utils.get_unique_path(dst_path)

        with open(dst_path, "w") as file:
            json.dump(profile, file)
        return dst_path

    def download_profile(self, filename: Optional[str] = None) -> Union[Dict, str]:
        """
        Returns the downloaded profile, either in memory or as a file.

        If the job is not ready, this function will block until completion.

        Parameters
        ----------
        filename : Optional[str]
            If filename is specified the profile is downloaded to file, otherwise to memory.

        Returns
        -------
        : Union[Dict, str]
            The downloaded profile, or filename
        """
        status = self.wait()
        profile = {}
        if status.success:
            res_pb = _api_call(api.get_job_results, self._owner.config, self.job_id)
            if res_pb.WhichOneof("result") == "profile_job_result":
                profile = _profile_pb_to_python_dict(res_pb.profile_job_result.profile)
                if filename is not None:
                    return self._write_profile(profile, filename)
            else:
                raise UserError("The supplied job ID is not for a Profile job")

        return profile

    def get_target_model(self) -> Optional[Model]:
        """
        Returns the target model object.
        If the job is not ready, this function will block until completion.

        Returns
        -------
        : Optional[TargetModel]
            The target model object, or None if the job failed.
        """
        status = self.wait()
        if status.success:
            if self._target_model is None:
                profile_job_pb = _api_call(
                    api.get_job, self._owner.config, job_id=self.job_id
                ).profile_job
                if profile_job_pb.HasField("target_model"):
                    self._target_model = self._owner._make_model(
                        profile_job_pb.target_model
                    )
                else:
                    raise APIException(
                        "We were unable to retreive the target model. Please contact us for help."
                    )

        return self._target_model

    def download_target_model(
        self, filename: Optional[str] = None
    ) -> Optional[Union[TargetModel, str]]:
        """
        Returns the downloaded target model, either in memory or as a file.

        If the job is not ready, this function will block until completion.

        Parameters
        ----------
        filename : Optional[str]
            If filename is specified the target model is downloaded to file, otherwise to memory.

            A filename must be provided in the following cases:
              - Target model is a MLModel and user is on Windows OS.
              - Target model is a compiled MLModel (.mlmodelc)

        Returns
        -------
        : Optional[Union[TargetModel, str]]
            The downloaded target model, filename, or None if the job failed.
        """
        target_model = self.get_target_model()
        if target_model is None:
            return None
        return target_model.download(filename)

    def download_results(self, artifacts_dir: str) -> ProfileJobResult:
        """
        Returns all the results of a job.

        This includes the profile and the compiled target model.

        If the job is not ready, this function will block until completion.

        Parameters
        ----------
        artifacts_dir : str
            Directory name where the job artifacts are stored.
            If the directory does not exist, it is cretaed.

        Returns
        -------
        : ProfileJobResult
            Job results.
        """
        if artifacts_dir is None:
            raise UserError("Must provide a valid directory to store artifacts.")

        artifacts_dir = os.path.abspath(os.path.expanduser(artifacts_dir))
        os.makedirs(artifacts_dir, exist_ok=True)

        profile = self.download_profile()
        assert isinstance(profile, Dict)
        self.download_target_model(artifacts_dir)
        self._write_profile(profile, artifacts_dir)

        return ProfileJobResult(
            status=self.get_status(),
            url=self.url,
            artifacts_dir=artifacts_dir,
            profile=profile,
        )

    def __str__(self) -> str:
        return f"Job(job_id={self.job_id}, model_id={self.model.model_id}, device={self.device}"

    def __repr__(self) -> str:
        return _class_repr_print(
            self,
            [
                "job_id",
                "url",
                ("status", self.get_status().code),
                "model",
                "name",
                "shapes",
                "device",
                "date",
            ],
        )


class ValidationJob(Job):
    """
    Validation job for a model, user provided inputs, and a device.

    A validation job should not be constructed directly. It is constructed by the hub client
    through :py:func:`tetra_hub.submit_validation_job`, :py:func:`tetra_hub.get_job`, or
    :py:func:`tetra_hub.get_jobs`.

    Attributes
    ----------
    job_id : str
        The job ID.
    device : Device
        The device for this job.
    model : Model
        The model for the job.
    name : str
        Name of this job
    date : datetime
        The time this job was submitted.
    inputs : Dataset
        The inputs provided by user.
    options: str
        Options passed during the job submission.
    """

    __in_progress_states: ClassVar[List[JobStatus.State]] = [
        JobStatus.State.PROVISIONING_DEVICE,
        JobStatus.State.VALIDATING_MODEL,
    ]
    __job_type_str = "validation"

    def __init__(
        self,
        owner: Client,
        job_id: str,
        device: Device,
        model: Model,
        name: str,
        date: datetime,
        options: str,
        verbose: bool,
        inputs: Dataset,
    ):
        super().__init__(
            owner=owner,
            job_id=job_id,
            device=device,
            model=model,
            name=name,
            date=date,
            options=options,
            verbose=verbose,
            job_type=self.__job_type_str,
            in_progress_states=self.__in_progress_states,
        )
        self.inputs = inputs
        self._outputs: Optional[Dataset] = None
        self._job_type = "validation"

    def get_output_dataset(self) -> Optional[Dataset]:
        """
        Returns the output dataset for a job.

        If the job is not ready, this function will block until completion.

        Returns
        -------
        : Optional[Dataset]
            The output data if the job succeeded
        """
        if not self._outputs:
            status = self.wait()
            if status.success:
                result = _api_call(api.get_job_results, self._owner.config, self.job_id)
                self._outputs = self._owner.get_dataset(
                    result.validation_job_result.output_dataset_id
                )

        return self._outputs

    def download_output_data(
        self, filename: Optional[str] = None
    ) -> Optional[Union[DatasetEntries, str]]:
        """
        Returns the downloaded output data, either in memory or as a h5f file.

        If the job is not ready, this function will block until completion.

        Parameters
        ----------
        filename : Optional[str]
            If filename is specified the output data is downloaded to file, otheriwse to memory.

        Returns
        -------
        : Optional[Union[DatasetEntries, str]]
            The downloaded output data, filename, or None if the job failed.
        """
        dataset = self.get_output_dataset()

        if dataset is None:
            return None
        else:
            return dataset.download(filename)

    def download_results(self, artifacts_dir: str) -> ValidationJobResult:
        """
        Returns all the results of a validation job.

        If the job is not ready, this function will block until completion.

        Parameters
        ----------
        artifacts_dir : str
            Directory name where the job artifacts are stored.
            If the directory does not exist, it is cretaed.

        Returns
        -------
        : ValidationJobResult
            Job results.
        """
        if artifacts_dir is None:
            raise UserError("Must provide a valid directory to store results.")

        artifacts_dir = os.path.abspath(os.path.expanduser(artifacts_dir))
        os.makedirs(artifacts_dir, exist_ok=True)

        self.download_output_data(artifacts_dir)

        return ValidationJobResult(
            status=self.get_status(), url=None, artifacts_dir=artifacts_dir
        )

    def __str__(self) -> str:
        return f"Job(job_id={self.job_id}, model_id={self.model.model_id}, device={self.device}, inputs={self.inputs}"

    def __repr__(self) -> str:
        if self.get_status().failure:
            return _class_repr_print(
                self,
                [
                    "job_id",
                    ("status", self.get_status().code),
                    ("failure_reason", self.get_status().message),
                    "model",
                    "name",
                    "inputs",
                    "device",
                    "date",
                ],
            )

        return _class_repr_print(
            self,
            [
                "job_id",
                ("status", self.get_status().code),
                "model",
                "name",
                "inputs",
                "device",
                "date",
            ],
        )


class Client:
    """
    Client object to interact with the Tetra Hub API.

    A default client, using credentials from ``~/.tetra/client.ini`` can be
    accessed through the ``tetra_hub`` module::

        import tetra_hub as hub

        # Calls Client.upload_model on a default Client instance.
        hub.upload_model("model.pt")
    """

    # Note: This class is primarily used through a default instantiation
    # through hub (e.g. import tetra_hub as hub; hub.upload_model(...)). For that
    # reason, all examples and cross references should point to tetra_hub for
    # documentation generation purposes.

    def __init__(self, config: Optional[ClientConfig] = None, verbose: bool = False):
        self._config = config
        self.verbose = verbose

    @property
    def config(self) -> ClientConfig:
        if self._config is None:
            try:
                self._config = _api_call(api.utils.load_default_api_config)
            except FileNotFoundError as e:
                raise UserError(
                    "Failed to load client configuration file.\n"
                    + _visible_textbox(str(e))
                )
        return self._config

    @staticmethod
    def _creation_date_from_timestamp(
        pb: Union[api_pb.Dataset, api_pb.ProfileJob, api_pb.ValidationJob, api_pb.Model]
    ) -> datetime:
        return datetime.fromtimestamp(pb.creation_time.seconds)

    @staticmethod
    def _expiration_date_from_timestamp(pb: api_pb.Dataset) -> datetime:
        return datetime.fromtimestamp(pb.expiration_time.seconds)

    def _web_url_of_job(self, job_id: str) -> str:
        # Final empty '' is to produce a trailing slash (esthetic choice)
        return urljoin(self.config.web_url, posixpath.join("jobs", job_id, ""))

    def set_verbose(self, verbose: bool = True) -> None:
        """
        If true, API calls may print progress to standard output.

        Parameters
        ----------
        verbose : bool
            Verbosity.

        """
        self.verbose = verbose

    def _get_devices(
        self,
        name: str = "",
        os: str = "",
        attributes: Union[str, List[str]] = [],
        select: bool = False,
    ) -> List[Device]:
        def _validate_interval(os: str) -> None:
            if len(os) > 0 and os[0] == "[":
                e = os.split("[", 1)
                if len(e) == 2 and len(e[0]) == 0:
                    e = e[1].split(",")
                    v = type(pv("0"))
                    if len(e) == 2 and (len(e[0]) == 0 or type(pv(e[0])) is v):
                        e = e[1].rsplit(")", 1)
                        if (
                            len(e) == 2
                            and len(e[1]) == 0
                            and (len(e[0]) == 0 or type(pv(e[0])) is v)
                        ):
                            return
                raise UserError(f"Incorrectly formed OS interval {os}")

        if isinstance(attributes, str):
            attributes = [attributes]
        _validate_interval(os)
        devices_pb = _api_call(
            api.get_device_list, self.config, name, os, attributes, select=select
        )
        devices = []
        for dev in devices_pb.devices:
            attrs = [a for a in dev.attributes]
            devices.append(Device(dev.name, dev.os, attrs))
        return devices

    def get_devices(
        self, name: str = "", os: str = "", attributes: Union[str, List[str]] = []
    ) -> List[Device]:
        """
        Returns a list of available devices.

        The returned list of devices are compatible with the supplied
        name, os, and attributes.
        The name must be an exact match with an existing device and os can either be a
        version ("15.2") or a version range ("[14,15)").

        Parameters
        ----------
        name : str
            Only devices with this exact name will be returned.
        os : str
            Only devices with an OS version that is compatible with this os are returned
        attributes : str|List[str]
            Only devices that have all requested properties are returned.

        Returns
        -------
        device_list : List[Device]
            List of available devices, comptatible with the supplied filters.

        Examples
        --------
        ::

            import tetra_hub as hub

            # Get all devices
            devices = hub.get_devices()

            # Get all devices matching this operating system
            devices = hub.get_devices(os="15.2")

            # Get all devices matching this chipset
            devices = hub.get_devices(attributes=["chipset:apple-a15"])

            # Get all devices matching hardware
            devices = hub.get_devices(name="Apple iPhone 12")
        """
        return self._get_devices(name, os, attributes)

    def _get_device(self, device: Device) -> Optional[Device]:
        devices = self._get_devices(device.name, device.os, device.attributes, True)
        assert len(devices) <= 1
        return devices[0] if len(devices) == 1 else None

    def get_device_attributes(self) -> List[str]:
        """
        Returns the super set of available device attributes.

        Any of these attributes can be used to filter devices when using
        :py:func:`~tetra_hub.get_devices`.

        Returns
        -------
        attribute_list : List[str]
            Super set of all available device attributes.

        Examples
        --------
        ::

            import tetra_hub as hub
            attributes = hub.get_device_attributes()

        """
        attrs = set()
        for d in self.get_devices():
            attrs |= set(d.attributes)
        attributes = list(attrs)
        attributes.sort()
        return attributes

    ## model related members ##
    def _make_model(
        self, model_pb: api_pb.Model, model: Optional[SourceModel] = None
    ) -> Model:
        date = self._creation_date_from_timestamp(model_pb)

        model_type = _get_source_model_type_from_model_type(model_pb.model_type)

        return Model(
            self,
            model_pb.model_id,
            date,
            model_type,
            model_pb.name,
            model,
            self.verbose,
        )

    def _upload_model(
        self,
        model: Union[Model, Any, str],  # Any instead of SourceModel to keep mypy happy
        model_type: SourceModelType,
        name: Optional[str] = None,
    ) -> Model:
        if isinstance(model, Model):
            return model
        suffix = _determine_model_extension(model_type)
        api_model_type = cast("api_pb.ModelType.ValueType", model_type.value)
        # delete=False to be compatible with Windows
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as file:
            path = file.name

        if isinstance(model, str):
            path = model
            model_name = os.path.basename(model)
            model = None
            if model_type == SourceModelType.MLMODELC:
                if not _is_valid_zipped_mlmodelc(path):
                    raise UserError(
                        f"Incorrect mlmodelc.zip provided. {ESPRESSO_NET_FILE} not found at the root level."
                    )
        elif model_type == SourceModelType.TORCHSCRIPT:
            import torch

            torch.jit.save(model, path)
            model_name = model.original_name
        elif model_type == SourceModelType.MLMODEL:
            model.save(path)
            # TODO: Figure out a better default name for MLModel instances
            model_name = "MLModel"
        elif model_type == SourceModelType.TFLITE:
            with open(path, "wb") as f:
                f.write(model)
            # TODO: Figure out a better default name for TFLite instances
            model_name = "TFLite"

        model_name = name or model_name
        res_pb = _api_call(
            api.create_and_upload_model,
            self.config,
            path,
            name=model_name,
            model_type=api_model_type,
            verbose=self.verbose,
        )

        os.remove(file.name)

        if res_pb.id:
            model_pb = api_pb.Model(
                model_id=res_pb.id,
                name=model_name,
                creation_time=res_pb.creation_time,
                model_type=api_model_type,
            )
            return self._make_model(model_pb, model)

        raise InternalError("Failed to upload model.")

    def upload_model(
        self, model: Union[SourceModel, str], name: Optional[str] = None
    ) -> Model:
        """
        Uploads a model.

        Parameters
        ----------
        model : SourceModel | str
            In memory representation or filename of the model to upload.
        name : Optional[str]
            Optional name of the model. If a name is not specified, it is decided
            either based on the model or the file name.

        Returns
        -------
        model : Model
            Returns a model if successful.

        Raises
        ------
        UserError
            Failure in the model input.

        Examples
        --------
        ::

            import tetra_hub as hub
            import torch

            pt_model = torch.jit.load("model.pt")

            # Upload model
            model = hub.upload_model(pt_model)

            # Jobs can now be scheduled using this model
            device = hub.Device("Apple iPhone 13 Pro", "15.2")
            job = hub.submit_profile_job(model, device=device,
                                         name="pt_model (1, 3, 256, 256)",
                                         input_shapes=[(1, 3, 256, 256)])

        """
        model_type = _determine_model_type(model)
        return self._upload_model(model, model_type, name)

    def _make_dataset(
        self, dataset_pb: api_pb.Dataset, data: Optional[DatasetEntries] = None
    ) -> Dataset:
        creation_date = self._creation_date_from_timestamp(dataset_pb)
        expiration_date = self._expiration_date_from_timestamp(dataset_pb)
        return Dataset(
            self,
            dataset_id=dataset_pb.dataset_id,
            dataset_name=dataset_pb.name,
            creation_time=creation_date,
            expiration_time=expiration_date,
            verbose=self.verbose,
            data=data,
        )

    def _upload_dataset(
        self, inputs: Union[Dataset, DatasetEntries, str], name: Optional[str] = None
    ) -> Dataset:
        if isinstance(inputs, Dataset):
            return inputs
        # delete=False to be compatible with Windows
        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as file:
            path = file.name

        if isinstance(inputs, str):
            path = inputs
            data_name = os.path.basename(inputs)
            data = None
        else:
            data_name = "h5-dataset"
            data = inputs
            with h5py.File(path, "w") as h5f:
                dataset_entries_to_h5(data, h5f)

        name = name or data_name
        res_pb = _api_call(
            api.create_and_upload_dataset,
            self.config,
            path,
            name,
            verbose=self.verbose,
        )

        os.remove(file.name)

        if res_pb.id:
            dataset_pb = api_pb.Dataset(
                dataset_id=res_pb.id,
                creation_time=res_pb.creation_time,
                expiration_time=res_pb.expiration_time,
                name=name,
            )
            return self._make_dataset(dataset_pb, data)

        raise InternalError("Failed to upload data.")

    def upload_dataset(
        self, data: Union[DatasetEntries, str], name: Optional[str] = None
    ) -> Dataset:
        """
        Upload a dataset.

        Parameters
        ----------
        data : OrderedDict[str, List[np.ndarray]] | OrderedDict[str, np.ndarray] | Dict[str, List[np.ndarray]] | Dict[str, np.ndarray] | str
            In memory representation or filename of the data to upload.
        name : Optional[str]
            Optional name of the dataset. If a name is not specified, it is decided
            either based on the data or the file name.

        Returns
        -------
        dataset : Dataset
            Returns a dataset object if successful.

        Examples
        --------
        ::

            import tetra_hub as hub
            import numpy as np

            # Define dataset
            array = np.reshape(np.array(range(15)), (3, 5)).astype(np.float32)
            input = {'x': [array]}

            # Upload dataset
            hub.upload_dataset(input, 'simplenet_dataset')
        """
        # TODO: Also, accept dataset from Torch Dataset. (#1824)
        self._check_data_entries(data)
        return self._upload_dataset(data, name)

    def get_datasets(self, offset: int = 0, limit: int = 50) -> List[Dataset]:
        """
        Returns a list of datasets visible to you.

        Parameters
        ----------
        offset : int
            Offset the query to get even older datasets.
        limit : int
            Maximum numbers of datasets to return.

        Returns
        -------
        dataset_list: List[Dataset]
            List of datasets.

        Examples
        --------
        Fetch :py:class:`Dataset` objects for your five most recent datasets::

            import tetra_hub as hub

            datasets = hub.get_datasets(limit=5)
        """
        datasets = []
        if limit > 0:
            dataset_pb = _api_call(
                api.get_dataset_list, self.config, offset=offset, limit=limit
            )
            datasets = [self._make_dataset(dataset) for dataset in dataset_pb.datasets]

        return datasets

    def get_dataset(self, dataset_id: str) -> Dataset:
        """
        Returns a dataset for a given id.

        Parameters
        ----------
        dataset_id : str
            id of a dataset.

        Returns
        -------
        dataset: Dataset
            The dataset for the id.

        Examples
        --------
        Get dataset and print information about it (it will not work for you)::

            import tetra_hub as hub

            dataset = hub.get_dataset("rmg9lg7y")
            print("Dataset information:", dataset)
        """
        dataset_pb = _api_call(api.get_dataset, self.config, dataset_id=dataset_id)
        return self._make_dataset(dataset_pb)

    def get_model(self, model_id: str) -> Model:
        """
        Returns a model for a given id.

        Parameters
        ----------
        model_id : str
            id of a model.

        Returns
        -------
        model: Model
            The model for the id.

        """
        model_pb = _api_call(api.get_model, self.config, model_id=model_id)
        return self._make_model(model_pb)

    def get_models(self, offset: int = 0, limit: int = 50) -> List[Model]:
        """
        Returns a list of models.

        Parameters
        ----------
        offset : int
            Offset the query to get even older models.
        limit : int
            Maximum numbers of models to return.

        Returns
        -------
        model_list: List[Model]
            List of models.

        Examples
        --------
        Fetch :py:class:`Model` objects for your five most recent models::

            import tetra_hub as hub

            models = hub.get_models(limit=5)

        """
        models = []
        if limit > 0:
            model_list_pb = _api_call(
                api.get_model_list, self.config, offset=offset, limit=limit
            )
            for model_pb in model_list_pb.models:
                models.append(self._make_model(model_pb))
        return models

    ## job related members ##
    def _make_job(
        self,
        job_pb: api_pb.Job,
        model: Optional[Model] = None,
        dataset: Optional[Dataset] = None,
    ) -> Job:

        if job_pb.WhichOneof("job") == "profile_job":
            profile_job_pb = job_pb.profile_job
            model = model or self._make_model(profile_job_pb.model)
            shapes = api.utils.tensor_type_list_pb_to_list_shapes(
                profile_job_pb.tensor_type_list
            )
            date = self._creation_date_from_timestamp(profile_job_pb)
            attrs = [a for a in profile_job_pb.device.attributes]
            device = Device(profile_job_pb.device.name, profile_job_pb.device.os, attrs)
            return ProfileJob(
                owner=self,
                shapes=shapes,
                job_id=profile_job_pb.profile_job_id,
                device=device,
                model=model,
                target_model=self._make_model(profile_job_pb.target_model)
                if profile_job_pb.HasField("target_model")
                else None,
                name=profile_job_pb.name,
                date=date,
                options=profile_job_pb.options,
                verbose=self.verbose,
            )
        elif job_pb.WhichOneof("job") == "validation_job":
            validation_job_pb = job_pb.validation_job
            model = model or self._make_model(validation_job_pb.model)
            dataset = dataset or self._make_dataset(validation_job_pb.dataset)
            date = self._creation_date_from_timestamp(validation_job_pb)
            attrs = [a for a in validation_job_pb.device.attributes]
            device = Device(
                validation_job_pb.device.name, validation_job_pb.device.os, attrs
            )
            return ValidationJob(
                owner=self,
                job_id=validation_job_pb.validation_job_id,
                device=device,
                model=model,
                name=validation_job_pb.name,
                date=date,
                options=validation_job_pb.options,
                inputs=dataset,
                verbose=self.verbose,
            )
        else:
            raise InternalError("Failed to create the job.")

    def get_job(self, job_id: str) -> Job:
        """
        Returns a job for a given id.

        Parameters
        ----------
        job_id : str
            id of a job.

        Returns
        -------
        job: Job
            The job for the id.

        Examples
        --------
        Get job and print its status (this job ID may not work for you)::

            import tetra_hub as hub

            job = hub.get_job("rmg9lg7y")
            status = job.get_status()
        """
        job_pb = _api_call(api.get_job, self.config, job_id=job_id)
        return self._make_job(job_pb)

    def get_jobs(self, offset: int = 0, limit: int = 50) -> List[Job]:
        """
        Returns a list of jobs visible to you.

        Parameters
        ----------
        offset : int
            Offset the query to get even older jobs.
        limit : int
            Maximum numbers of jobs to return.

        Returns
        -------
        job_list: List[Job]
            List of jobs.

        Examples
        --------
        Fetch :py:class:`ProfileJobResult` objects for your five most recent jobs::

            import tetra_hub as hub

            jobs = hub.get_jobs(limit=5)
            results = [job.download_results("results") for job in jobs]
        """
        jobs = []
        if limit > 0:
            job_list_pb = _api_call(
                api.get_job_list, self.config, offset=offset, limit=limit
            )
            for job_pb in job_list_pb.jobs:
                jobs.append(self._make_job(job_pb))
        return jobs

    def _check_input_shapes(
        self,
        model_type: SourceModelType,
        input_shapes: Optional[Shapes] = None,
        inputs: Optional[Union[Dataset, DatasetEntries]] = None,
    ) -> None:
        if inputs is not None:
            self._check_data_entries(inputs)
            if input_shapes is not None and not api.utils.do_input_shapes_match(
                input_shapes, api.utils.convert_inputs_to_tensor_type_list_pb(inputs)
            ):
                raise UserError("input_shapes must match provided inputs.")

        if model_type == SourceModelType.TORCHSCRIPT:
            if (input_shapes is None or not any(input_shapes)) and inputs is None:
                raise UserError("input_shapes must be provided for TorchScript models.")
            if not isinstance(input_shapes, OrderedDict) and not isinstance(
                input_shapes, list
            ):
                raise UserError(
                    "input_shapes for TorchScript models must be a List[Tuple[int, ...] or OrderedDict[str, Tuple[int, ...]] or List[Tuple[str, Tuple[int, ...]]]."
                )
        elif model_type == SourceModelType.MLMODEL:
            if (
                input_shapes is not None
                and isinstance(input_shapes, list)
                and any(input_shapes)
                and not isinstance(input_shapes[0][0], str)
            ):
                raise UserError(
                    "input_shapes must have names for Core ML model inputs."
                )
        elif model_type == SourceModelType.TFLITE:
            if input_shapes is not None and not (
                isinstance(input_shapes, list)
                and all(
                    isinstance(elem, tuple)
                    and len(elem) > 0
                    and all(isinstance(t, int) for t in elem)
                    for elem in input_shapes
                )
            ):
                raise UserError(
                    "input_shapes for TFLite models must be a List[Tuple[int, ...]."
                )

    def _check_data_entries(self, inputs: Union[Dataset, DatasetEntries, str]) -> None:
        if isinstance(inputs, Dataset):
            return
        if isinstance(inputs, str):
            _, suffix = os.path.splitext(inputs)
            if suffix != ".h5":
                raise UserError('Dataset file must have ".h5" extension.')
            return
        if not isinstance(inputs, Dict):
            raise UserError(
                "inputs for Core ML model must be a dictionary with key as input name and value as list of numpy arrays or a numpy array. The list of numpy arrays denotes multiple data points. Each datapoint must an element of this list and represented as a numpy array."
            )
        batchsizes: set[int] = set()
        for value in inputs.values():
            if isinstance(value, np.ndarray):
                value = [value]
            if isinstance(value, list) and all(
                isinstance(data, np.ndarray) and data.dtype == np.dtype("float32")
                for data in value
            ):
                batchsizes |= set([len(value)])
            else:
                raise UserError(
                    "The values in inputs dictionary must be list of numpy arrays or a single numpy array, with type float32."
                )
        if len(batchsizes) > 1:
            raise UserError("Batchsize of all inputs must be the same.")

    def _create_tensor_type_list(
        self,
        input_shapes: Optional[Shapes] = None,
        inputs: Optional[Union[DatasetEntries, Dataset]] = None,
    ) -> Optional[api_pb.NamedTensorTypeList]:
        if inputs is not None:
            return api.utils.convert_inputs_to_tensor_type_list_pb(inputs)
        elif input_shapes is not None:
            return api.utils.list_shapes_to_tensor_type_list_pb(input_shapes)
        else:
            return None

    def _check_devices(
        self, device: Union[Device, List[Device]], model_type: SourceModelType
    ) -> List[Device]:
        if isinstance(device, Device):
            device = [device]
        devices = []
        for dev in device:
            d = self._get_device(dev)
            if d is None:
                raise UserError(f"{dev} is not available.")
            else:
                devices.append(d)
            if (
                model_type == SourceModelType.MLMODEL
                and "framework:coreml" not in d.attributes
            ):
                raise UserError(f"device {d} does not support Core ML model input")
            if (
                model_type == SourceModelType.TFLITE
                and "framework:tflite" not in d.attributes
            ):
                raise UserError(f"device {d} does not support TFLite model input")
        return devices

    def submit_validation_job(
        self,
        model: Union[Model, SourceModel, str],
        device: Union[Device, List[Device]],
        inputs: Union[Dataset, DatasetEntries, str],
        name: Optional[str] = None,
        options: Optional[str] = None,
    ) -> Union[Job, List[Job]]:
        """
        Submits a validation job.

        Parameters
        ----------
        model : Model | SourceModel | str
            Model to validate (must be CoreML format, path to CoreML model, or a Model object from a profiling job).
        devices : Device | List[Device]
            Devices on which to run the job.
        inputs: str | OrderedDict[str, List[np.ndarray]] | OrderedDict[str, np.ndarray] | Dict[str, List[np.ndarray]] | Dict[str, np.ndarray] | Dataset
            The inputs can be a filename or a dict/OrderedDict, where the keys are the
            names of the features and the values are the tensors. Each tensor can be one of

            - numpy array (single input).
            - list of numpy arrays (batch input)
        name : None | str
            Optional name for the job. Job names need not be unique.
        options : None | str
            Cli-like flag options.

        Returns
        -------
        job: Job | List[Job]
            Returns the validation jobs.

        Examples
        --------
        Submit a Core ML model for validation on an iPhone 11::

            import tetra_hub as hub
            import coremltools as ct
            import numpy as np
            from typing import OrderedDict

            # Load an MLModel
            ml_model = ct.models.MLModel("squeeze_net.mlmodel")

            # Setup input data
            input_tensor = np.random.random((1, 3, 227, 227)).astype(np.float32)
            input_data = OrderedDict({"image": input_tensor})

            # Submit validation job
            job = hub.submit_validation_job(ml_model,
                               device=hub.Device("Apple iPhone 11", "14.0"),
                               name="squeeze_net (1, 3, 227, 227)",
                               inputs=input_data)

        For more examples, see :ref:`examples`.
        """

        # Determine the model type
        model_type = _determine_model_type(model)
        if model_type == SourceModelType.TORCHSCRIPT:
            raise UserError("TorchScript models cannot be used for validation.")

        devices = self._check_devices(device, model_type)
        self._check_data_entries(inputs)
        model = self._upload_model(model, model_type=model_type)
        dataset = self._upload_dataset(inputs)

        job_name = name if name else model.name
        jobs = []
        for dev in devices:
            dev_pb = api_pb.Device(name=dev.name, os=dev.os)
            for attr in dev.attributes:
                dev_pb.attributes.append(attr)
            model_pb = api_pb.Model(model_id=model.model_id)
            dataset_pb = api_pb.Dataset(dataset_id=dataset.dataset_id)
            validation_job_pb = api_pb.ValidationJob(
                model=model_pb,
                name=job_name,
                device=dev_pb,
                dataset=dataset_pb,
                options=options if options else "",
            )
            response_pb = _api_call(
                api.create_validation_job, self.config, validation_job_pb
            )
            validation_job_pb.validation_job_id = response_pb.id
            validation_job_pb.creation_time.CopyFrom(response_pb.creation_time)
            job_pb = api_pb.Job(validation_job=validation_job_pb)
            job = self._make_job(job_pb, model, dataset)
            jobs.append(job)
            if self.verbose:
                base_url = "/".join(job.url.split("/")[:-2])
                msg = (
                    f"Scheduled job ({job.job_id}) successfully. To see "
                    "the status and results:\n"
                    f"    {base_url}\n"
                )
                print(msg)

        return jobs[0] if len(jobs) == 1 else jobs

    def submit_profile_job(
        self,
        model: Union[Model, SourceModel, str],
        device: Union[Device, List[Device]],
        name: Optional[str] = None,
        input_shapes: Optional[Shapes] = None,
        options: Optional[str] = None,
    ) -> Union[Job, List[Job]]:
        """
        Submits a profiling job.

        Parameters
        ----------
        model : Model | SourceModel | str
            Model to profile.
        devices : Device | List[Device]
            Devices on which to run the job.
        name : None | str
            Optional name for the job. Job names need not be unique.
        input_shapes : None | Dict[str, Tuple[int, ...]] | List[Tuple[int, ...]] | OrderedDict[str, Tuple[int, ...]]]] | List[Tuple[str, Tuple[int, ...]]] | Dataset
            When the SourceModel is a PyTorch model, the input_shapes can be a list of tuples (one for each input) or an OrderedDict
            where the keys are the (optional) names of the features. These names are used for input nodes in the compiled Core ML model.
            Setting input_shapes to dictionary without ordering is not supported for PyTorch models.

            When the SourceModel is a Core ML model, the input_shapes can be set to None (inferred from the model) or a dict/OrderedDict,
            where the keys are the names of the features and values are the shapes. Setting input_shapes to List[Tuples] without names
            is not supported for Core ML models.
        options : None | str
            Cli-like flag options.

        Returns
        -------
        job: Job | List[Job]
            Returns the profile jobs.

        Examples
        --------
        Submit a traced Torch model for profiling on an iPhone 11::

            import tetra_hub as hub
            import torch

            pt_model = torch.jit.load("mobilenet.pt")

            input_shapes = (1, 3, 224, 224)

            model = hub.upload_model(pt_model)

            job = hub.submit_profile_job(model, device=hub.Device("Apple iPhone 11", "14.0"),
                                         name="mobilenet (1, 3, 224, 224)",
                                         input_shapes=[input_shapes])

        For more examples, see :ref:`examples`.
        """
        # Determine the model type
        model_type = _determine_model_type(model)
        devices = self._check_devices(device, model_type)
        self._check_input_shapes(model_type=model_type, input_shapes=input_shapes)
        model = self._upload_model(model, model_type=model_type)
        tensor_type_list_pb = self._create_tensor_type_list(input_shapes=input_shapes)

        job_name = name if name else model.name
        jobs = []
        for dev in devices:
            dev_pb = api_pb.Device(name=dev.name, os=dev.os)
            for attr in dev.attributes:
                dev_pb.attributes.append(attr)
            model_pb = api_pb.Model(model_id=model.model_id)
            profile_job_pb = api_pb.ProfileJob(
                model=model_pb,
                name=job_name,
                device=dev_pb,
                tensor_type_list=tensor_type_list_pb,
                options=options if options else "",
            )
            response_pb = _api_call(api.create_profile_job, self.config, profile_job_pb)
            profile_job_pb.profile_job_id = response_pb.id
            profile_job_pb.creation_time.CopyFrom(response_pb.creation_time)
            job_pb = api_pb.Job(profile_job=profile_job_pb)
            job = self._make_job(job_pb, model)
            jobs.append(job)
            if self.verbose:
                msg = (
                    f"Scheduled job ({job.job_id}) successfully. To see "
                    "the status and results:\n"
                    f"    {job.url}\n"
                )
                print(msg)

        return jobs[0] if len(jobs) == 1 else jobs


__all__ = [
    "Error",
    "InternalError",
    "UserError",
    "Device",
    "Model",
    "Job",
    "ProfileJob",
    "ValidationJob",
    "SourceModelType",
    "JobResult",
    "ProfileJobResult",
    "ValidationJobResult",
    "JobStatus",
    "Shapes",
    "Dataset",
]
