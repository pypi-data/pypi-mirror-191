from typing import Dict, Any, List

from algora.api.service.datasets.v2.dataset_asset.model import DatasetAssetRequest
from algora.api.service.datasets.v2.model import SearchRequest
from algora.common.decorators import async_data_request
from algora.common.function import no_transform
from algora.api.service.datasets.v2.dataset_asset.__util import (
    _get_dataset_asset_request_info,
    _get_dataset_assets_request_info,
    _search_dataset_assets_request_info,
    _create_dataset_asset_request_info,
    _update_dataset_asset_request_info,
    _delete_dataset_asset_request_info,
)
from algora.common.requests import (
    __async_get_request,
    __async_post_request,
    __async_put_request,
    __async_delete_request,
)


@async_data_request(transformers=[no_transform])
async def async_get_dataset_asset(id: str) -> Dict[str, Any]:
    """
    Asynchronously get dataset asset by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _get_dataset_asset_request_info(id)
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_get_dataset_assets() -> List[Dict[str, Any]]:
    """
    Asynchronously get all dataset assets.

    Returns:
        List[Dict[str, Any]]: List of dataset asset response
    """
    request_info = _get_dataset_assets_request_info()
    return await __async_get_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_search_dataset_assets(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all dataset assets.

    Args:
        request (SearchRequest): Dataset asset search request

    Returns:
        List[Dict[str, Any]]: List of dataset asset response
    """
    request_info = _search_dataset_assets_request_info(request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_create_dataset_asset(request: DatasetAssetRequest) -> Dict[str, Any]:
    """
    Asynchronously create dataset asset.

    Args:
        request (DatasetAssetRequest): Dataset asset request

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _create_dataset_asset_request_info(request)
    return await __async_put_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_update_dataset_asset(
    id: str, request: DatasetAssetRequest
) -> Dict[str, Any]:
    """
    Asynchronously update dataset asset.

    Args:
        id (str): Dataset ID
        request (DatasetAssetRequest): Dataset asset request

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _update_dataset_asset_request_info(id, request)
    return await __async_post_request(**request_info)


@async_data_request(transformers=[no_transform])
async def async_delete_dataset_asset(id: str) -> None:
    """
    Asynchronously delete dataset asset by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        None
    """
    request_info = _delete_dataset_asset_request_info(id)
    return await __async_delete_request(**request_info)
