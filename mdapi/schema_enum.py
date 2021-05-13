from typing import Optional, Literal
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


LinksKey = Literal[
    "al", "ap", "bw", "cdj", "mu", "nu", "kt", "amz", "ebj", "mal",
    "raw", "engtl", "dj"
]
LanguageCode = Optional[Literal[
    "en", "pt-br", "ru", "fr", "es-la", "pl", "tr", "it", "es", "id", "vi",
    "hu", "zh", "ar", "de", "zh-hk", "ca", "th", "bg", "fa", "uk", "mn", "he",
    "ro", "ms", "tl", "ja", "ko", "hi", "my", "cs", "pt", "nl", "sv", "bn",
    "no", "lt", "el", "sr", "da", "fi",
]]
SortOrder = Literal["asc", "desc"]

Version = Optional[conint(ge=1)]
