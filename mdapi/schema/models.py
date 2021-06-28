from mdapi.endpoints import Endpoints
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

    def relations_to(self, type_: str):
        if self.relationships is None:
            return []
        return [i for i in self.relationships if i.type == type_]


Type = KeyedUnion[BaseType]


class User(BaseType):
    _type = "user"

    id: Optional[str]
    username: str


class Tag(BaseType):
    _type = "tag"

    name: LocalizedString
    description: List[LocalizedString]
    group: Optional[str]


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

    @property
    def tag_names(self):
        return [i.name for i in self.tags]

    @property
    def authors(self):
        return self.relations_to("author")

    @property
    def artists(self):
        return self.relations_to("artist")


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

    @property
    def groups(self):
        return self.relations_to("scanlation_group")

    @property
    def manga(self):
        if (manga := self.relations_to("manga")):
            return manga[0]
        return None

    @property
    def uploader(self):
        if (users := self.relations_to("user")):
            return users[0]
        return None


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


class Cover(BaseType):
    _type = "cover_art"

    volume: Optional[str]
    fileName: str
    description: str
    createdAt: datetime
    updatedAt: datetime

    @property
    def manga(self):
        return self.relations_to("manga")[0]

    @property
    def url(self):
        return Endpoints.COVERS.format(self.manga.id, self.fileName)

    @property
    def url_512(self):
        return self.url + ".512.jpg"

    @property
    def url_256(self):
        return self.url + ".256.jpg"


class UploadSession(BaseType):
    _type = "upload_session"

    isCommitted: bool
    isProcessed: bool
    isDeleted: bool


class UploadSessionFile(BaseType):
    _type = "upload_session_file"

    originalFileName: str
    fileHash: str
    fileSize: int
    mimeType: str
