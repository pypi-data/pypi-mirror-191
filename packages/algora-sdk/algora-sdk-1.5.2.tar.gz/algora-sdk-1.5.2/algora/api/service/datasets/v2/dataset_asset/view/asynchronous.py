from typing import Dict, Any, List

from algora.api.service.datasets.v2.model import SearchRequest
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.api.service.datasets.v2.dataset_asset.view.__util import (
    _get_dataset_asset_view_request_info,
    _get_dataset_asset_views_request_info,
    _search_dataset_asset_views_request_info,
)
from algora.common.requests import (
    __async_get_request,
    __async_post_request,
)


@async_data_request(transformers=[no_transform])
async def async_get_dataset_asset_view(id: str) -> Dict[str, Any]:
    """
    Asynchronously get dataset asset view by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        Dict[str, Any]: Dataset asset view response
    """
    request_info = _get_dataset_asset_view_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_dataset_asset_views() -> List[Dict[str, Any]]:
    """
    Asynchronously get all dataset asset views.

    Returns:
        List[Dict[str, Any]]: List of dataset asset view response
    """
    request_info = _get_dataset_asset_views_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_search_dataset_asset_views(
    request: SearchRequest,
) -> List[Dict[str, Any]]:
    """
    Asynchronously search all dataset asset views.

    Args:
        request (SearchRequest): Dataset asset view search request

    Returns:
        List[Dict[str, Any]]: List of dataset asset view response
    """
    request_info = _search_dataset_asset_views_request_info(request)
    return await __async_post_request(**request_info)
