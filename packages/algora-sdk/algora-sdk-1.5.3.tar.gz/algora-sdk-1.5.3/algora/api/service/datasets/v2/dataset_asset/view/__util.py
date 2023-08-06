from algora.api.service.datasets.v2.model import SearchRequest


def _get_dataset_asset_view_request_info(id: str) -> dict:
    return {"endpoint": f"config/v2/dataset/asset/view/{id}"}


def _get_dataset_asset_views_request_info() -> dict:
    return {"endpoint": f"config/v2/dataset/asset/view"}


def _search_dataset_asset_views_request_info(request: SearchRequest) -> dict:
    return {
        "endpoint": f"config/v2/dataset/asset/view/search",
        "json": request.request_dict(),
    }
