import pandas as pd
from algora.common.function import data_required_transform
from requests import Response

from algora.api.data.query.__util import (
    _query_datasets_request_info,
    _query_dataset_csv_request_info,
    _query_timeseries_request_info,
    _query_timeseries_v2_request_info,
)
from algora.api.data.query.model import TimeseriesQueryRequest
from algora.common.decorators import async_data_request
from algora.common.requests import __async_post_request, __async_get_request


async def async_query_dataset(id: str, data=None, json=None) -> Response:
    """
    Asynchronously query dataset by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST
        json (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_datasets_request_info(id, data, json)
    return await __async_post_request(**request_info)


async def async_query_dataset_csv(id: str, data=None) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, data)
    return await __async_get_request(**request_info)


@async_data_request
def async_query_timeseries(request: TimeseriesQueryRequest) -> pd.DataFrame:
    """
    Asynchronously query timeseries dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_request_info(request)
    return __async_post_request(**request_info)


@async_data_request(transformers=[data_required_transform])
def query_timeseries_v2(request: TimeseriesQueryRequest) -> pd.DataFrame:
    """
    Query timeseries v2 dataset by timeseries query request.

    Args:
        request (TimeseriesQueryRequest): Timeseries query request

    Returns:
        pd.DataFrame: Timeseries DataFrame
    """
    request_info = _query_timeseries_v2_request_info(request)
    return __async_post_request(**request_info)
