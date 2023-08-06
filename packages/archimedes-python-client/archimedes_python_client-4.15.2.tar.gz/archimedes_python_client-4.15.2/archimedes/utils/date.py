from datetime import datetime
from typing import Union

import pandas as pd

from archimedes import ArchimedesConstants


def get_start_date(start) -> pd.Timestamp:
    """
    Args:
        start (str): The start date provided by the user

    Returns:
        pd.Timestamp: start date given in string form to pd.Timestamp. If not given,
                      or empty, it returns ArchimedesConstants.DATE_LOW
    """
    return pd.to_datetime(start, utc=True) if start else ArchimedesConstants.DATE_LOW


def get_end_date(end) -> pd.Timestamp:
    """
    Args:
        end (str): The end date provided by the user

    Returns:
        pd.Timestamp: end date given in string form to pd.Timestamp. If not given,
                      or empty, it returns ArchimedesConstants.DATE_HIGH
    """
    return pd.to_datetime(end, utc=True) if end else ArchimedesConstants.DATE_HIGH


def datetime_to_iso_format(
    datetime_str_pandas_timestamp_or_none: Union[str, pd.Timestamp, datetime, None]
) -> Union[str, None]:
    """
    Take one of str, pd.Timestamp, datetime and convert it to str in iso format.

    Args:
        datetime_str_pandas_timestamp_or_none(str, pd.Timestamp, datetime, None):
            Input datetime.

    Returns:
        (str, None):
            string representation of the date in iso format.
    """
    return (
        pd.to_datetime(datetime_str_pandas_timestamp_or_none, utc=True).isoformat()
        if datetime_str_pandas_timestamp_or_none is not None
        else None
    )
