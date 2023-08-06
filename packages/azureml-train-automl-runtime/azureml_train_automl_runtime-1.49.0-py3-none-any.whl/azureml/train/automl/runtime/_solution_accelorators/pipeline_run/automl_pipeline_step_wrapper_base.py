# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Class for AutoML pipeline step wrapper base class.
"""
from typing import Optional
from abc import ABC, abstractmethod
import logging
import sys

from azureml.core import Run
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared._diagnostics.automl_events import RunSucceeded, RunFailed
from azureml.automl.core._logging.event_logger import EventLogger

from ..utilities import logging_utilities as lu
from ..utilities import run_utilities as ru


logger = logging.getLogger(__name__)


class AutoMLPipelineStepWrapperBase(ABC):
    def __init__(self, step_name: str, current_step_run: Optional[Run] = None):
        """
        Wrapper base class for AutoML pipeline runs.

        :param step_name: The step name.
        :param current_step_run: The current run step.
        """
        self.step_name = step_name
        self.arguments_dict = ru.get_arguments_dict(step_name, self.is_prs_step())
        self.event_logger_dim = lu.get_additional_logging_custom_dim(step_name)
        self.step_run = self._get_current_step_run(current_step_run, self.is_prs_step())
        self.event_logger = EventLogger(self.step_run)

    def _get_current_step_run(self, current_step_run: Optional[Run] = None, stagger: bool = True) -> Run:
        """
        Get current step run for the wrapper.

        :param current_step_run: The run object. If is not none, this run will be used.
        :param stagger: The switch controls whether the run is obtained use a staggered call.
        :return: The current step run object.
        """
        if current_step_run is None:
            if stagger:
                ru.stagger_randomized_secs(self.arguments_dict)
            current_step_run = Run.get_context()
        return current_step_run

    def run(self) -> None:
        """The run wrapper."""
        try:
            lu.init_logger(
                module=sys.modules[__name__], handler_name=__name__,
                custom_dimensions=self.event_logger_dim, run=self.step_run)
            logger.info("{} wrapper started.".format(self.step_name))
            self._run()
            logger.info("{} wrapper completed.".format(self.step_name))
            self.event_logger.log_event(RunSucceeded(
                self.step_run.id,
                lu.get_event_logger_additional_fields(self.event_logger_dim, self.step_run.parent.id)))
        except Exception as e:
            error_code, error_str = run_lifecycle_utilities._get_error_code_and_error_str(e)
            failure_event = RunFailed(
                run_id=self.step_run.id, error_code=error_code, error=error_str,
                additional_fields=lu.get_event_logger_additional_fields(
                    self.event_logger_dim, self.step_run.parent.id))
            run_lifecycle_utilities.fail_run(self.step_run, e, failure_event=failure_event)
            raise

    @abstractmethod
    def is_prs_step(self) -> bool:
        """Whether the step is prs or not."""
        pass

    @abstractmethod
    def _run(self) -> None:
        """The actual run script."""
        pass
