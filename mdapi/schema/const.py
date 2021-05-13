from typing import Optional, Literal, TypeVar, Union
from enum import Enum

from pydantic import conint


class PublicationDemographic(Enum):
    shounen = "shounen"
    shoujo = "shoujo"
    josei = "josei"
    seinen = "seinen"


class Status(Enum):
    ongoing = "ongoing"
    completed = "completed"
    hiatus = "hiatus"
    cancelled = "cancelled"

    hitaus = "hitaus"


class ContentRating(Enum):
    safe = "safe"
    suggestive = "suggestive"
    erotica = "erotica"
    pornographic = "pornographic"


class ReadingStatus(Enum):
    reading = "reading"
    on_hold = "on_hold"
    plan_to_read = "plan_to_read"
    dropped = "dropped"
    re_reading = "re_reading"
    completed = "completed"


class CustomListVisibility(Enum):
    public = "public"
    private = "private"


class MultiMode(Enum):
    AND = "AND"
    OR = "OR"


class LegacyType(Enum):
    group = "group"
    manga = "manga"
    chapter = "chapter"
    tag = "tag"


class SortOrder(Enum):
    asc = "asc"
    desc = "desc"


class LinksKey(Enum):
    anilist = "al"
    animeplanet = "ap"
    bookwalker = "bw"
    cdJapan = "cdj"
    mangaUpdates = "mu"
    novelUpdates = "nu"
    kitsu = "kt"
    amazon = "amz"
    ebookJapan = "ebj"
    myAnimeList = "mal"
    raw = "raw"
    officialEn = "engtl"
    doujinshi = "dj"


class UnsetValue(type):
    ...


T = TypeVar("T")
CanUnset = Union[T, UnsetValue]

LanguageCode = Optional[Literal[
    "en", "pt-br", "ru", "fr", "es-la", "pl", "tr", "it", "es", "id", "vi",
    "hu", "zh", "ar", "de", "zh-hk", "ca", "th", "bg", "fa", "uk", "mn", "he",
    "ro", "ms", "tl", "ja", "ko", "hi", "my", "cs", "pt", "nl", "sv", "bn",
    "no", "lt", "el", "sr", "da", "fi",
]]

Version = Optional[conint(ge=1)]
Year = conint(ge=1, le=9999)
