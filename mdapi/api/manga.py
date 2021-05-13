from typing import Dict, List, Optional
from datetime import datetime

from pydantic import validate_arguments

from ..util import PaginatedRequest, is_actually
from ..endpoints import Endpoints
from ..schema import (
    MultiMode, Status, LanguageCode, PublicationDemographic, Type, Tag, Year,
    ContentRating, TypeOrId, MangaSortOrder, ReadingStatus, Author, Manga,
    LinksKey, Version, CustomList, LocalizedString
)
from .base import APIBase


class MangaAPI(APIBase):
    def _search(self, **kwargs):
        return PaginatedRequest(
            self.api, Endpoints.Manga.SEARCH, params=kwargs
        )

    @validate_arguments
    @is_actually(_search)
    def search(
        self,
        title: Optional[str] = None,
        authors: Optional[List[TypeOrId[Author]]] = None,
        artists: Optional[List[TypeOrId]] = None,
        year: Optional[Year] = None,
        includedTags: Optional[List[TypeOrId[Tag]]] = None,
        includedTagsMode: Optional[MultiMode] = None,
        excludedTags: Optional[List[TypeOrId[Tag]]] = None,
        excludedTagsMode: Optional[MultiMode] = None,
        status: Optional[Status] = None,
        originalLanguage: Optional[LanguageCode] = None,
        publicationDemographic: Optional[PublicationDemographic] = None,
        ids: Optional[List[TypeOrId[Manga]]] = None,
        contentRating: Optional[ContentRating] = None,
        createdAtSince: Optional[datetime] = None,
        updatedAtSince: Optional[datetime] = None,
        order: Optional[MangaSortOrder] = None,
        limit: int = 10,
        offset: int = 0,
    ):
        ...

    @validate_arguments
    def get(self, manga: TypeOrId[Manga]) -> Manga:
        return Type.parse_obj(self.api._make_request(
            Endpoints.Manga.GET,
            urlparams={"manga": manga}
        ))

    @validate_arguments
    def delete(self, manga: TypeOrId[Manga]) -> None:
        self.api._make_request(
            Endpoints.Manga.DELETE,
            urlparams={"manga": manga}
        )

    @validate_arguments
    def follow(self, manga: TypeOrId[Manga]) -> None:
        self.api._make_request(
            Endpoints.Manga.FOLLOW,
            urlparams={"manga": manga}
        )

    @validate_arguments
    def unfollow(self, manga: TypeOrId[Manga]) -> None:
        self.api._make_request(
            Endpoints.Manga.UNFOLLOW,
            urlparams={"manga": manga}
        )

    def all_tags(self) -> List[Tag]:
        return [
            Type.parse_obj(i.get("data"))
            for i in self.api._make_request(Endpoints.Manga.TAGS)
        ]

    def random(self) -> Manga:
        return Type.parse_obj(self.api._make_request(Endpoints.Manga.RANDOM))

    def _create(self, **kwargs):
        kwargs["version"] = 1
        return self.api._make_request(Endpoints.Manga.CREATE, kwargs)

    @validate_arguments
    @is_actually(_create)
    def create(
        self,
        title: LocalizedString,
        altTitles: List[LocalizedString],
        description: LocalizedString,
        authors: List[TypeOrId[Author]],
        artists: List[TypeOrId],
        links: List[Dict[LinksKey, str]],
        originalLanguage: LanguageCode,
        year: Year,
        lastVolume: Optional[str] = None,
        lastChapter: Optional[str] = None,
        publicationDemographic: Optional[PublicationDemographic] = None,
        status: Optional[Status] = None,
        contentRating: Optional[ContentRating] = None,
    ) -> Manga:
        ...

    def _edit(self, **kwargs):
        manga = kwargs.pop("id")
        return self.api._make_request(
            Endpoints.Manga.EDIT, kwargs,
            urlparams={"manga": manga},
            keep_null=True
        )

    @validate_arguments
    @is_actually(_edit)
    def edit(
        self,
        manga: TypeOrId[Manga],
        title: LocalizedString,
        altTitles: List[LocalizedString],
        description: LocalizedString,
        authors: List[TypeOrId[Author]],
        artists: List[TypeOrId],
        links: List[Dict[LinksKey, str]],
        originalLanguage: LanguageCode,
        year: Year,
        version: Version,
        lastVolume: Optional[str] = None,
        lastChapter: Optional[str] = None,
        publicationDemographic: Optional[PublicationDemographic] = None,
        status: Optional[Status] = None,
        contentRating: Optional[ContentRating] = None,
    ) -> Manga:
        ...

    @validate_arguments
    def get_chapters(
        self,
        manga: TypeOrId[Manga],
        locales: Optional[List[LanguageCode]] = None
    ) -> PaginatedRequest:
        return PaginatedRequest(
            self.api,
            Endpoints.Manga.CHAPTERS,
            limit=500,
            urlparams={"manga": manga},
            params={"locales": locales}
        )

    @validate_arguments
    def get_read(self, manga: TypeOrId[Manga]):
        return self.api._make_request(
            Endpoints.Manga.MARK_READ,
            urlparams={"manga": manga}
        )

    @validate_arguments
    def set_status(self, manga: TypeOrId[Manga], status: ReadingStatus):
        return self.api._make_request(
            Endpoints.Manga.SET_STATUS,
            urlparams={"manga": manga},
            body={"status": status}
        )

    @validate_arguments
    def add_to_list(self, manga: TypeOrId[Manga], list: TypeOrId[CustomList]):
        self.api._make_request(
            Endpoints.Manga.ADD_TO_LIST,
            urlparams={"manga": manga, "list": list}
        )

    @validate_arguments
    def remove_from_list(
        self, manga: TypeOrId[Manga], list: TypeOrId[CustomList]
    ):
        self.api._make_request(
            Endpoints.Manga.REMOVE_FROM_LIST,
            urlparams={"manga": manga, "list": list}
        )
