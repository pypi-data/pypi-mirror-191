import os
import sys
import logging
import pandas as pd

from markus_pettersen.general import camel_to_snake


# Setup root logger
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL,
)
LOG = logging.getLogger(__name__)


def unpack_nested_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Unpack nested column from a dataframe.
    Removes the nested column.

    Args:
        df (pd.DataFrame): Dataframe with of a CDF object
        column (List[str]): Column to unpack

    Returns:
        pd.Dataframe: Dataframe with the column unpacked
    """
    return pd.concat([df, pd.json_normalize(df[column])], axis=1).drop(columns=column)


def get_batch(df: pd.DataFrame, ids: dict[str, list[str]], start_key: str) -> pd.DataFrame:
    """
    Get batch given the provided ids

    Args:
        df (pd.DataFrame): The full dataframe
        ids (dict[str, list[str]]): Dictionary with ids and the name of the corresponding column
        start_key (str): The name of the first id column

    Returns:
        pd.DataFrame: A batch of the dataframe
    """
    comparison = df[start_key].isin(ids[start_key])
    for k, v in ids.items():
        if k == start_key:
            continue
        comparison &= df[k].isin(v)
    return df.loc[comparison]


def fix_columns(df: pd.DataFrame, target_columns: list[str]) -> pd.DataFrame:
    """
    Fix columns with a .value suffix

    Args:
        df (pd.DataFrame): A dataframe
        target_columns (list[str]): The columns to keep

    Returns:
        pd.DataFrame: Dataframe with the fixed columns
    """
    df.columns = [
        camel_to_snake(col.replace('.value', ''))
        for col in df.columns
    ]
    return df[[col for col in target_columns if col in df.columns]]


def filter_reference(df: pd.DataFrame, col: str, values: list):
    return df.loc[df[col].isin(values)]
