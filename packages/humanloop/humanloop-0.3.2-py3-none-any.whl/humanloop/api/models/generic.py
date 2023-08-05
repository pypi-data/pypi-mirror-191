from typing import Generic, List, TypeVar

from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class PaginatedData(GenericModel, Generic[DataT]):
    records: List[DataT]
    page: int
    size: int
    total: int
