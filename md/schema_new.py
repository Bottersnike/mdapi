from typing import List, Optional
from pydantic import BaseModel

from .schema import (
    LocalizedString, PublicationDemographic, Status, ContentRating
)


class NewManga(BaseModel):
    title: LocalizedString
    altTitles: List[LocalizedString]
    description: LocalizedString
    authors: List[str] = []
    artists: List[str] = []
    originalLanguage: str
    lastVolume: Optional[int]
    lastChapter: Optional[int]
    publicationDemographic: Optional[PublicationDemographic]
    status: Optional[Status]
    year: Optional[int]
    contentRating: Optional[ContentRating]
    modNotes: Optional[str]


class EditManga(NewManga):
    id: str
