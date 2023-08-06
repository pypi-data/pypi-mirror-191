from typing import Dict, Any, List

from algora.api.service.datasets.v2.dataset_asset.view.__util import (
    _get_dataset_asset_view_request_info,
    _get_dataset_asset_views_request_info,
    _search_dataset_asset_views_request_info,
)
from algora.api.service.datasets.v2.model import SearchRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __get_request,
    __post_request,
)


@data_request(transformers=[no_transform])
def get_dataset_asset_view(id: str) -> Dict[str, Any]:
    """
    Get dataset asset view by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        Dict[str, Any]: Dataset asset view response
    """
    request_info = _get_dataset_asset_view_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_dataset_asset_views() -> List[Dict[str, Any]]:
    """
    Get all dataset asset views.

    Returns:
        List[Dict[str, Any]]: List of dataset asset view response
    """
    request_info = _get_dataset_asset_views_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def search_dataset_asset_views(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all dataset asset views.

    Args:
        request (SearchRequest): Dataset asset view search request

    Returns:
        List[Dict[str, Any]]: List of dataset asset view response
    """
    request_info = _search_dataset_asset_views_request_info(request)
    return __post_request(**request_info)
