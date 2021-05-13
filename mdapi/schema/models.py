from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, constr
from uuid import UUID

from .util import LocalizedString, KeyedUnion
from .const import (
    LanguageCode, LinksKey, PublicationDemographic, Status, ContentRating,
    ReadingStatus, CustomListVisibility, Version, Year, LegacyType
)


class Relationship(BaseModel):
    id: str
    type: str


class BaseType(BaseModel):
    id: str
    relationships: Optional[List[Relationship]] = []
    version: Version


Type = KeyedUnion[BaseType]


class User(BaseType):
    _type = "user"

    id: Optional[str]
    username: str


class Tag(BaseType):
    _type = "tag"

    name: LocalizedString
    # restricted: Optional[bool]


class Manga(BaseType):
    _type = "manga"

    title: LocalizedString
    altTitles: List[LocalizedString]
    description: LocalizedString
    isLocked: bool
    originalLanguage: LanguageCode
    tags: List[Type]

    lastVolume: Optional[str]
    lastChapter: Optional[str]
    links: Optional[Dict[LinksKey, str]]
    publicationDemographic: Optional[PublicationDemographic]
    status: Optional[Status]
    year: Optional[Year]
    contentRating: Optional[ContentRating]
    readingStatus: Optional[ReadingStatus]

    createdAt: datetime
    updatedAt: datetime


class Chapter(BaseType):
    _type = "chapter"

    title: constr(max_length=255)
    volume: Optional[str]
    chapter: Optional[constr(max_length=8)]
    translatedLanguage: Optional[LanguageCode]

    hash: str
    data: List[str]
    dataSaver: List[str]

    uploader: Optional[UUID]
    createdAt: datetime
    updatedAt: datetime
    publishAt: datetime


class ScanlationGroup(BaseType):
    _type = "scanlation_group"

    name: str
    leader: Type
    createdAt: datetime
    updatedAt: datetime


class CustomList(BaseType):
    _type = "custom_list"

    name: str
    visibility: CustomListVisibility
    owner: Type


class MappingID(BaseType):
    _type = "mapping_id"

    type: LegacyType
    legacyId: int
    newId: str


class Author(BaseType):
    _type = "author"

    name: str
    biography: List[LocalizedString]
    imageUrl: Optional[str]
    createdAt: datetime
    updatedAt: datetime