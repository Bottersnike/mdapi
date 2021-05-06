from typing import Any, List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel


PublicationDemographic = Literal["shounen", "shoujo", "josei", "seinen"]
Status = Literal["ongoing", "completed", "hiatus", "abandoned"]
ReadingStatus = Literal[
    "reading", "on_hold", "plan_to_read", "dropped", "re_reading", "completed"
]
ContentRating = Literal["safe", "suggestive", "erotica", "pornographic"]
CustomListVisibility = Literal["public", "private"]


class LocalizedString(dict):
    def __init__(self, text, lang="en"):
        self.lang = lang
        self.text = text

    def items(self):
        return [(self.lang, self.text)]

    def keys(self):
        return [self.lang]

    def values(self):
        return [self.text]

    def __pretty__(self, fmt, **kwargs):
        yield "<"
        yield self.lang
        yield " "
        yield fmt(self.text)
        yield ">"

    def __getitem__(self, key):
        if key != self.lang:
            raise ValueError
        return self.text

    def __str__(self):
        return self.text

    @classmethod
    def __get_validators__(cls):
        yield cls.return_i18n

    @classmethod
    def return_i18n(cls, values):
        return cls(*list(values.items())[0][::-1])


class Type_:
    @classmethod
    def __get_validators__(cls):
        yield cls.return_type

    @classmethod
    def return_type(cls, values):
        _TYPES = {
            "author": Author,
            "chapter": Chapter,
            "manga": Manga,
            "user": User,
            "scanlation_group": ScanlationGroup,
            "tag": Tag,
            "custom_list": CustomList,
            "mapping_id": MappingID,
        }

        if "type" not in values:
            return None
        type = values["type"]

        if type not in _TYPES:
            raise KeyError(f"Incorrect type: {type}")
        return _TYPES[type](
            id=values["id"],
            relationships=values.get("relationships"),
            **values["attributes"]
        )


class Type(BaseModel):
    __root__: Type_

    def __new__(cls, *args, **kwargs):
        (self := object.__new__(cls)).__init__(*args, **kwargs)
        return self.__root__

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __getattr__(self, item):
        return getattr(self.__root__, item)

    def dict(self):
        return self.__root__.dict()


class Relationship(BaseModel):
    id: str
    type: str


class BaseType(BaseModel):
    id: str
    relationships: Optional[List[Relationship]] = []
    version: Optional[int]


class User(BaseType):
    id: Optional[str]
    username: str


class Manga(BaseType):
    type = "manga"

    title: LocalizedString
    altTitles: List[LocalizedString]
    description: LocalizedString
    isLocked: bool
    links: Optional[Any]
    originalLanguage: str
    lastVolume: Optional[str]
    lastChapter: Optional[str]
    publicationDemographic: Optional[PublicationDemographic]
    status: Optional[Status]
    year: Optional[int]
    contentRating: Optional[ContentRating]
    tags: List[Any]
    createdAt: datetime
    updatedAt: datetime
    readingStatus: Optional[ReadingStatus]


class Chapter(BaseType):
    type = "chapter"

    volume: Optional[str]
    chapter: str
    title: Optional[str]
    translatedLanguage: str
    hash: str
    data: List[str]
    dataSaver: Optional[List[str]]
    publishAt: datetime
    createdAt: datetime
    updatedAt: datetime


class ScanlationGroup(BaseType):
    type = "scanlation_group"

    name: str
    leader: Type
    createdAt: datetime
    updatedAt: datetime


class Tag(BaseType):
    type = "tag"

    name: LocalizedString
    restricted: bool


class CustomList(BaseType):
    type = "custom_list"

    name: str
    visibility: CustomListVisibility
    owner: Type


class MappingID(BaseType):
    type = "mapping_id"

    legacyId: int
    newId: str


class Author(BaseType):
    type = "author"

    name: str
    imageUrl: Optional[str]
    biography: List[LocalizedString]
    createdAt: datetime
    updatedAt: datetime
