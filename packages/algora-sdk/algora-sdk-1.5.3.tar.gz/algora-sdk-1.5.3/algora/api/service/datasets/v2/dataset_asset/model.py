from typing import Optional, List, Dict

from algora.api.service.datasets.v2.model import Field, TimeseriesFilter
from algora.common.base import Base
from algora.common.enum import Order


class DatasetAssetRequest(Base):
    asset_id: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: Optional[List[str]]
    fields: Optional[List[Field]]
    where_clause: Optional[List[TimeseriesFilter]]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Optional[Dict[str, Order]]
    dataset_id: str


class DatasetAssetResponse(Base):
    id: str
    asset_id: str
    display_name: str
    description: Optional[str]
    filter_field: str
    tags: List[str]
    fields: Optional[List[Field]]
    where_clause: Optional[List[TimeseriesFilter]]
    row_limit: Optional[int]
    max_limit: Optional[int]
    sort: Dict[str, Order]
    dataset_id: str
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
