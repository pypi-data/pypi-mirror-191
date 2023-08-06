from typing import Optional, List, Dict

from algora.api.service.datasets.v2.model import Field, TimeseriesFilter
from algora.common.base import Base
from algora.common.enum import Order


class DatasetAssetViewResponse(Base):
    id: str
    asset_id: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: List[str]
    fields: Optional[List[Field]]
    where_clause: List[TimeseriesFilter]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    dataset_id: str
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
