from algora.api.service.datasets.v2.dataset_asset.model import DatasetAssetRequest
from algora.api.service.datasets.v2.model import SearchRequest


def _get_dataset_asset_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/asset/{id}"}


def _get_dataset_assets_request_info() -> dict:
    return {"endpoint": f"config/v2/dataset/asset"}


def _search_dataset_assets_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/v2/dataset/asset/search",
        "json": request.request_dict(),
    }


def _create_dataset_asset_request_info(request: DatasetAssetRequest) -> dict:
    return {"endpoint": f"config/v2/dataset/asset", "json": request.request_dict()}


def _update_dataset_asset_request_info(id: str, request: DatasetAssetRequest) -> dict:
    return {"endpoint": f"config/v2/dataset/asset/{id}", "json": request.request_dict()}


def _delete_dataset_asset_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/asset/{id}"}
