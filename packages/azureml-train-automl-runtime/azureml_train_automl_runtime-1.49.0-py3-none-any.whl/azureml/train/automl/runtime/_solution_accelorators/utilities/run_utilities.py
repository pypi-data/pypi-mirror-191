# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, Any, List, Optional, cast, Union
import json
from random import randint
import os
from time import sleep
import argparse
import hashlib

from azureml.core import Run
from azureml.train.automl.constants import HTSConstants
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import UserException
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared._diagnostics.automl_error_definitions import HierarchyAllParallelRunsFailedByUserError

from ..data_models.status_record import StatusRecord


def stagger_randomized_secs(arguments_dict: Dict[str, Any]) -> None:
    """
    Stagger the node for the a randomized seconds based on preocess_count_per_node and nodes_count.

    :param arguments_dict: The arguements_dict contains all the running arguemnts.
    """
    max_concurrent_runs = arguments_dict.get("process_count_per_node", 10)
    node_count = int(arguments_dict.get(HTSConstants.NODES_COUNT, 1))
    traffic_ramp_up_period_in_seconds = min(max_concurrent_runs * node_count, 600)
    worker_sleep_time_in_seconds = randint(1, traffic_ramp_up_period_in_seconds)
    print("Traffic ramp up period: {} seconds".format(traffic_ramp_up_period_in_seconds))
    print(
        "Sleeping this worker for {} seconds to stagger traffic "
        "ramp-up...".format(worker_sleep_time_in_seconds))
    sleep(worker_sleep_time_in_seconds)


def get_arguments_dict(script_scenario: str, is_parallel_run_step: bool = False) -> Dict[str, str]:
    """
    Get the arguements dict for the driver script.

    :param script_scenario: The different scenarios.
    :param is_parallel_run_step: If the driver scripts is a pipeline run. Pipeline run will add some arguments other
                                 the the default ones.
    :return: Dict[str, str]
    """
    print("Loading arguments for scenario {}".format(script_scenario))
    argument_dict = {}
    parser = argparse.ArgumentParser("Parsing input arguments.")
    for arg in HTSConstants.HTS_SCRIPTS_SCENARIO_ARG_DICT[script_scenario]:
        print("adding argument {}".format(arg))
        parser.add_argument(arg, dest=HTSConstants.HTS_OUTPUT_ARGUMENTS_DICT[arg], required=False)
    parser.add_argument(
        "--process_count_per_node", default=1, type=int, help="number of processes per node", required=False)

    args, _ = parser.parse_known_args()
    if is_parallel_run_step:
        # process_count_per_node and nodes_count can be used for help with concurrency
        argument_dict["process_count_per_node"] = args.process_count_per_node

    for arg in HTSConstants.HTS_SCRIPTS_SCENARIO_ARG_DICT[script_scenario]:
        argument_dict[arg] = getattr(args, HTSConstants.HTS_OUTPUT_ARGUMENTS_DICT[arg])
    print("Input arguments dict is {}".format(argument_dict))

    return argument_dict


def get_model_hash(str_list: List[str]) -> str:
    """
    Get the model hash from a str list.

    :param str_list: The str list using for hast.
    :return: str
    """
    model_string = '_'.join(str(v) for v in str_list).lower()
    sha = hashlib.sha256()
    sha.update(model_string.encode())
    return sha.hexdigest()


def check_parallel_runs_status(status_records: List[StatusRecord], parallel_step: str, uploaded_file: str) -> None:
    """Check the results of all parallel runs."""
    Contract.assert_true(
        status_records is not None and len(status_records) > 0, message="Status records should not be empty.",
        reference_code=ReferenceCodes._HTS_RUNTIME_EMPTY_STATUS_RECORDS, log_safe=True)
    if all([sr.status == StatusRecord.FAILED for sr in status_records]):
        Contract.assert_true(
            all([sr.error_type == StatusRecord.USER_ERROR for sr in status_records]),
            message="Status records should not contain system errors.", log_safe=True,
            reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_SYSTEM_ERROR
        )
        raise UserException._with_error(
            AzureMLError.create(
                HierarchyAllParallelRunsFailedByUserError,
                target="status_record", parallel_step=parallel_step, file_name=uploaded_file,
                reference_code=ReferenceCodes._HTS_RUNTIME_STATUS_RECORDS_USER_ERROR
            )
        )


def get_input_dataset_name(input_dataset_name: Optional[str]) -> str:
    """
    Get the input dataset name.

    :param input_dataset_name: The input dataset name.
    :return: return HTSConstants.HTS_INPUT is input_input_dataset_name is None or '' or
        HTSConstants.DEFAULT_ARG_VALUE.
    """
    if input_dataset_name is None or input_dataset_name == '' or input_dataset_name == HTSConstants.DEFAULT_ARG_VALUE:
        return cast(str, HTSConstants.HTS_INPUT)
    return input_dataset_name


def str_or_bool_to_boolean(str_or_bool: Union[str, bool]) -> bool:
    """
    Convert the value which can be string or boolean to boolean.

    :param str_or_bool: the value, which can be string or boolean.
    :return: the corresponding boolean value.
    """
    return str_or_bool == 'True' or str_or_bool is True


def get_pipeline_run(run: Optional[Run] = None) -> Run:
    """
    Get the pipeline run.

    :param run: If run is passed in then use the property of that run,
    :return: Run
    """
    if run is None:
        run = Run.get_context()
    parent_run = Run(run.experiment, run.properties.get('azureml.pipelinerunid'))
    return parent_run


def get_parsed_metadata_from_artifacts(run: Run, output_dir: str) -> Dict[str, Any]:
    """
    Get the metadata parsed as a dict from artifacts.

    :param run: The pipeline run.
    :param output_dir: The temp output dir.
    :return: Dict[str, Any]
    """
    run.download_file(HTSConstants.HTS_FILE_PROPORTIONS_METADATA_JSON, output_dir)
    raw_metadata_file = os.path.join(output_dir, HTSConstants.HTS_FILE_PROPORTIONS_METADATA_JSON)
    with open(raw_metadata_file) as f:
        raw_metadata = json.load(f)

    parsed_metadata = {}
    for metadata_node in raw_metadata[HTSConstants.METADATA_JSON_METADATA]:
        node_id = metadata_node[HTSConstants.NODE_ID]
        parsed_metadata[node_id] = {
            HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE:
                metadata_node[HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE],
            HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS:
                metadata_node[HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS]
        }
    os.remove(raw_metadata_file)
    return parsed_metadata
