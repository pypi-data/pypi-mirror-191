# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Optional, List, Generator, Union, Tuple
import os
import pandas as pd

from azureml.train.automl.constants import HTSConstants
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet


def fill_na_with_space(df: pd.Series) -> pd.Series:
    """
    Fill na with space for a pandas columns

    :param df: The input dataframe.
    :return:  pd.DataFrame
    """
    if df.isna().any():
        return df.fillna(" ")
    else:
        return df


def concat_df_with_none(df: Optional[pd.DataFrame], update_df: pd.DataFrame) -> pd.DataFrame:
    """
    Concat two dataframes. If the first one is None, then return the second one. If not, return the concat result of
    these two dataframe.

    :param df: First pd.DataFrame that can be None.
    :param update_df: Second pd.DataFrame.
    :return: The concat pd.DataFrame of these two.
    """
    if df is None:
        return update_df
    else:
        return pd.concat([df, update_df], ignore_index=True)


def abs_sum_target_by_time(
        df: pd.DataFrame,
        time_column_name: str,
        label_column_name: str,
        other_column_names: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate the absolute sum value of a dataframe by the time_column_name.

    :param df: The input df.
    :param time_column_name: The time column name.
    :param label_column_name: The column name contains the values that needs to be take summation.
    :param other_column_names: Other column name that won't need group by.
    :return: pd.DataFrame
    """
    group_by_columns = [time_column_name]
    if other_column_names is not None:
        group_by_columns.extend(other_column_names)
    all_keep_columns = [col for col in group_by_columns]
    all_keep_columns.append(label_column_name)
    return df[all_keep_columns].groupby(group_by_columns).apply(lambda c: c.abs().sum()).reset_index()


def get_cross_time_df(
        df_sum: Optional[pd.DataFrame],
        df: pd.DataFrame,
        time_column_name: str,
        label_column_name: str
) -> pd.DataFrame:
    """
    Calculate the absolute summation of a pd.DataFrame with another dataframe based on time_column_name.

    :param df_sum: First pd.DataFrame which can be None.
    :param df: Second pd.DataFrame.
    :param time_column_name: The time column name.
    :param label_column_name: The column name contains the values that needs to be take summation.
    :return: pd.DataFrame
    """
    group_df_sum = abs_sum_target_by_time(df, time_column_name, label_column_name)
    if df_sum is None:
        return group_df_sum
    else:
        return abs_sum_target_by_time(
            pd.concat([df_sum, group_df_sum]), time_column_name, label_column_name)


def get_n_points(
        input_data: pd.DataFrame, time_column_name: str, label_column_name: str, freq: Optional[str] = None
) -> int:
    """
    Get a number of points based on a TimeSeriesDataFrame.

    :param input_data: The input data.
    :param time_column_name: The time column name.
    :param label_column_name: The label column name.
    :param freq: The user input frequency.
    :return: int
    """
    tsds = TimeSeriesDataSet(
        input_data.copy(), time_column_name=time_column_name, target_column_name=label_column_name
    )
    if freq is None:
        dataset_freq = tsds.infer_freq()
    else:
        dataset_freq = freq
    return len(pd.date_range(start=tsds.time_index.min(), end=tsds.time_index.max(), freq=dataset_freq))


def calculate_average_historical_proportions(
        n_points: int,
        df: pd.DataFrame,
        df_total: pd.DataFrame,
        time_column_name: str,
        label_column_name: str,
        hierarchy: List[str]
) -> pd.DataFrame:
    """
    Calculate average historical proportions based on two pd.DataFrames containing values after summation.

    :param n_points: number of total points
    :param df: The pd.DataFrame which taking summation by grouping the time column and bottom hierarchy level.
    :param df_total: The pd.DataFrame which taking summation by grouping the time column.
    :param time_column_name: The time column name.
    :param label_column_name: The column that contains the summations.
    :param hierarchy: The hierarchy column names.
    :return: pd.DataFrame
    """
    # Convert the time column to same type to avoid joining error
    df[time_column_name] = df[time_column_name].astype('object')
    df_total[time_column_name] = df_total[time_column_name].astype('object')
    df_total.rename(columns={label_column_name: HTSConstants.HTS_CROSS_TIME_SUM}, inplace=True)

    merged_df = pd.merge(df, df_total, how='left', on=[time_column_name])
    merged_df[HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS] = (
        merged_df[label_column_name] / merged_df[HTSConstants.HTS_CROSS_TIME_SUM] / n_points)
    all_final_column = [col for col in hierarchy]
    all_final_column.append(HTSConstants.AVERAGE_HISTORICAL_PROPORTIONS)
    cols_to_agg = set(all_final_column) - set(hierarchy)
    return merged_df[all_final_column]. \
        groupby(hierarchy, group_keys=False, as_index=False). \
        apply(lambda c: c[cols_to_agg].abs().sum())


def calculate_proportions_of_historical_average(
        df: pd.DataFrame, label_column_name: str, hierarchy: List[str], total_value: Union[float, int]
) -> pd.DataFrame:
    """
    Calculate proportions of historical average based on hierarchical timeseries allocation.

    :param df: The input pd.DataFrame.
    :param label_column_name: The column that needs to calculate the proportions of historical average.
    :param hierarchy: The hierarchy columns list.
    :param total_value: The total value which pha will be normalized by.
    :return: pd.DataFrame
    """
    all_final_column = [col for col in hierarchy]
    all_final_column.append(label_column_name)
    aggregated_df = df[all_final_column].groupby(hierarchy).apply(lambda c: c.abs().sum()).reset_index()
    aggregated_df[label_column_name] = aggregated_df[label_column_name] / total_value
    aggregated_df.rename(
        columns={label_column_name: HTSConstants.PROPORTIONS_OF_HISTORICAL_AVERAGE}, inplace=True)
    return aggregated_df


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load a csv file or a parquet file into memory as pd.DataFrame

    :param file_path: The file path.
    :return: pd.DataFrame
    """
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    if file_extension.lower() == ".parquet":
        data = pd.read_parquet(file_path)
    else:
        data = pd.read_csv(file_path)
    return data


def get_input_data_generator(local_file_path: str) -> Generator[Tuple[pd.DataFrame, str], None, None]:
    """
    Generate pd.DataFrame from an input dataset or a local file path.

    :param local_file_path: The dir contains all the local data files.
    :return: None
    """
    for file in os.listdir(local_file_path):
        print("Processing collected {}.".format(file))
        yield pd.read_csv(os.path.join(local_file_path, file)), file
