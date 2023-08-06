# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Optional, Dict
from types import ModuleType
import copy
import logging
import uuid

from azureml.core import Run
from azureml.automl.core.shared._diagnostics.automl_events import AutoMLBaseEvent
from azureml.automl.core.shared import log_server, logging_utilities
from azureml.telemetry import INSTRUMENTATION_KEY
from azureml.train.automl.constants import HTSConstants


def init_logger(
        module: Optional[ModuleType] = None,
        path: Optional[str] = None,
        handler_name: Optional[str] = None,
        run: Optional[Run] = None,
        custom_dimensions: Optional[Dict[str, str]] = None,
        verbosity: int = logging.INFO
) -> None:
    """
    Init logger for the pipeline run.

    :param module: The module name.
    :param path: The file path.
    :param handler_name: The name of the handler.
    :param run: an AzureML run.
    :param custom_dimensions: additional custom dimensions for logging.
    :param verbosity: The verbosity of the logs.
    :return:
    """
    if module is not None:
        logging_utilities.mark_package_exceptions_as_loggable(module)
    if path is not None:
        logging_utilities.mark_path_as_loggable(path)
    if handler_name is not None:
        log_server.install_sockethandler(handler_name)
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    if run is None:
        run = Run.get_context()
    current_custom_dim = {
        HTSConstants.LOGGING_RUN_ID: run.id,
        HTSConstants.LOGGING_PIPELINE_ID: run.properties.get('azureml.pipelinerunid'),
        HTSConstants.LOGGING_SUBSCRIPTION_ID: run.experiment.workspace.subscription_id,
        HTSConstants.LOGGING_REGION: run.experiment.workspace.location
    }
    if custom_dimensions:
        current_custom_dim.update(custom_dimensions)
    log_server.update_custom_dimensions(current_custom_dim)

    # Explicitly set verbosity
    log_server.set_verbosity(verbosity)


def get_additional_logging_custom_dim(sub_run_type: str) -> Dict[str, str]:
    """Get the additional properties for logging."""
    return {
        HTSConstants.LOGGING_SCRIPT_SESSION_ID: str(uuid.uuid4()),
        HTSConstants.LOGGING_RUN_SUBTYPE: sub_run_type,
        HTSConstants.LOGGING_RUN_TYPE: HTSConstants.RUN_TYPE
    }


def get_event_logger_additional_fields(
        custom_dim: Dict[str, str],
        pipeline_id: str,
        script_type: str = "run",
        should_emit: str = "True"
) -> Dict[str, str]:
    """Get the additional properties for event logger."""
    additional_fields = copy.deepcopy(custom_dim)
    additional_fields["hts_pipeline_id"] = pipeline_id
    additional_fields["hts_script_type"] = script_type
    additional_fields[AutoMLBaseEvent.SHOULD_EMIT] = should_emit
    return additional_fields


def update_log_custom_dimension(custom_dimension_dict: Dict[str, str]) -> None:
    """Update the custom dimension for log server."""
    log_server.update_custom_dimensions(custom_dimension_dict)
