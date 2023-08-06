# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Class for AutoML pipeline step wrapper base class.
"""
from typing import Optional
from abc import abstractmethod
import logging

from azureml.core import Run

from .automl_pipeline_step_wrapper_base import AutoMLPipelineStepWrapperBase


logger = logging.getLogger(__name__)


class AutoMLPythonStepWrapper(AutoMLPipelineStepWrapperBase):
    """Wrapper base class for AutoML Python script step runs."""
    def __init__(self, step_name: str, current_step_run: Optional[Run] = None):
        """
        Wrapper base class for AutoML Python script step runs.

        :param step_name: The step name.
        :param current_step_run: The current run step.
        """
        super(AutoMLPythonStepWrapper, self).__init__(step_name, current_step_run)

    def is_prs_step(self) -> bool:
        """Whether the step is prs or not."""
        return False

    @abstractmethod
    def _run(self) -> None:
        """The actual run script."""
        pass
