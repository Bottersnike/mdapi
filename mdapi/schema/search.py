from typing import Optional

from pydantic import BaseModel

from .const import SortOrder


class Paginated(BaseModel):
    limit: int = 10
    offset: int = 0


class BaseSortOrder(BaseModel):
    def serialize(self):
        return {
            f"order[{i}]": getattr(self, i, None)
            for i in self.__fields__
        }


class AuthorSortOrder(BaseSortOrder):
    name: Optional[SortOrder]


class MangaSortOrder(BaseSortOrder):
    createdAt: Optional[SortOrder]
    updatedAt: Optional[SortOrder]


class ChapterSortOrder(BaseSortOrder):
    createdAt: Optional[SortOrder]
    updatedAt: Optional[SortOrder]
    publishAt: Optional[SortOrder]
    volume: Optional[SortOrder]
    chapter: Optional[SortOrder]


class CoverSortOrder(BaseSortOrder):
    createdAt: Optional[SortOrder]
    updatedAt: Optional[SortOrder]
    volume: Optional[SortOrder]
