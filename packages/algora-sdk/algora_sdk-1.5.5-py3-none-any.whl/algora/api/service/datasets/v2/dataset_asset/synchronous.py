from typing import Dict, Any, List

from algora.api.service.datasets.v2.dataset_asset.__util import (
    _get_dataset_asset_request_info,
    _get_dataset_assets_request_info,
    _search_dataset_assets_request_info,
    _create_dataset_asset_request_info,
    _update_dataset_asset_request_info,
    _delete_dataset_asset_request_info,
)
from algora.api.service.datasets.v2.dataset_asset.model import DatasetAssetRequest
from algora.api.service.datasets.v2.model import SearchRequest
from algora.common.decorators import data_request
from algora.common.function import no_transform
from algora.common.requests import (
    __get_request,
    __post_request,
    __put_request,
    __delete_request,
)


@data_request(transformers=[no_transform])
def get_dataset_asset(id: str) -> Dict[str, Any]:
    """
    Get dataset asset by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _get_dataset_asset_request_info(id)
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def get_dataset_assets() -> List[Dict[str, Any]]:
    """
    Get all dataset assets.

    Returns:
        List[Dict[str, Any]]: List of dataset asset response
    """
    request_info = _get_dataset_assets_request_info()
    return __get_request(**request_info)


@data_request(transformers=[no_transform])
def search_dataset_assets(request: SearchRequest) -> List[Dict[str, Any]]:
    """
    Search all dataset assets.

    Args:
        request (SearchRequest): Dataset asset search request

    Returns:
        List[Dict[str, Any]]: List of dataset asset response
    """
    request_info = _search_dataset_assets_request_info(request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def create_dataset_asset(request: DatasetAssetRequest) -> Dict[str, Any]:
    """
    Create dataset asset.

    Args:
        request (DatasetAssetRequest): Dataset asset request

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _create_dataset_asset_request_info(request)
    return __put_request(**request_info)


@data_request(transformers=[no_transform])
def update_dataset_asset(id: str, request: DatasetAssetRequest) -> Dict[str, Any]:
    """
    Update dataset asset.

    Args:
        id (str): Dataset ID
        request (DatasetAssetRequest): Dataset asset request

    Returns:
        Dict[str, Any]: Dataset asset response
    """
    request_info = _update_dataset_asset_request_info(id, request)
    return __post_request(**request_info)


@data_request(transformers=[no_transform])
def delete_dataset_asset(id: str) -> None:
    """
    Delete dataset asset by ID.

    Args:
        id (str): Dataset asset ID

    Returns:
        None
    """
    request_info = _delete_dataset_asset_request_info(id)
    return __delete_request(**request_info)
