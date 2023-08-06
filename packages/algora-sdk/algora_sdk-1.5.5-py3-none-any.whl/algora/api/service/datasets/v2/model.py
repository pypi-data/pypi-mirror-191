from typing import Optional, List, Set, Dict, Any
from pydantic import Field as pyField

from algora.common.enum import FieldType, Order, SqlOperator

from algora.common.base import Base


class Field(Base):
    display_name: str
    logical_name: str
    type: FieldType
    width: int
    editable: bool
    hidden: bool
    tags: List[str]
    field_group_display_name: str
    field_group_logical_name: str


class TimeseriesFilter(Base):
    field: str
    operator: SqlOperator
    value: Any


class DatasetRequest(Base):
    dataset_id: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Set[TimeseriesFilter]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    tags: Set[str]
    schema_: Set[Field] = pyField(alias="schema")


class SearchRequest(Base):
    query: str
    tag: Optional[str]


class DatasetResponse(Base):
    id: str
    dataset_id: str
    display_name: str
    description: Optional[str]
    table_name: str
    where_clause: Set[TimeseriesFilter]
    row_limit: int
    max_limit: int
    sort: Dict[str, Order]
    tags: Set[str]
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]
    schema_: Set[Field] = pyField(alias="schema")
