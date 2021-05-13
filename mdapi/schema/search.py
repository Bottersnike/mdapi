from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from .const import (
    MultiMode, SortOrder, Status, LanguageCode, PublicationDemographic,
    ContentRating
)
from .util import TypeOrId


class Paginated(BaseModel):
    limit: int = 10
    offset: int = 0


class BaseSortOrder(BaseModel):
    def serialize(self):
        return {
            f"order[{i}]": getattr(self, i, None)
            for i in self.__fields__
        }


class MangaSortOrder(BaseSortOrder):
    createdAt: Optional[SortOrder]
    updatedAt: Optional[SortOrder]


class ChaptersListOrder(BaseSortOrder):
    createdAt: Optional[SortOrder]
    updatedAt: Optional[SortOrder]
    publishAt: Optional[SortOrder]
    volume: Optional[SortOrder]
    chaptert: Optional[SortOrder]


class MangaSearch(Paginated):
    title: Optional[str]
    authors: Optional[List[TypeOrId]]
    artists: Optional[List[TypeOrId]]
    year: Optional[int]
    includedTags: Optional[List[TypeOrId]]
    includedTagsMode: Optional[MultiMode]
    excludedTags: Optional[List[TypeOrId]]
    excludedTagsMode: Optional[MultiMode]
    status: Optional[Status]
    originalLanguage: Optional[LanguageCode]
    publicationDemographic: Optional[PublicationDemographic]
    ids: Optional[List[TypeOrId]]
    contentRating: Optional[ContentRating]
    createdAtSince: Optional[datetime]
    updatedAtSince: Optional[datetime]
    order: Optional[MangaSortOrder]

    def __init__(self, *args, **kwargs):
        pass
