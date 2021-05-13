from mdapi.schema.search import ChapterSortOrder
from typing import Dict, List
from datetime import datetime

from pydantic import validate_arguments

from ..util import PaginatedRequest, shadows
from ..endpoints import Endpoints
from ..schema import (
    MultiMode, Status, LanguageCode, PublicationDemographic, Type, Tag, Year,
    ContentRating, TypeOrId, MangaSortOrder, ReadingStatus, Author, Manga,
    LinksKey, Version, CustomList, LocalizedString, CanUnset
)
from .base import APIBase


class MangaAPI(APIBase):
    def _search(self, limit=None, offset=None, **kwargs):
        return PaginatedRequest(
            self.api, Endpoints.Manga.SEARCH, params=kwargs,
            limit=limit, offset=offset,
        )

    @validate_arguments
    @shadows(_search)
    def search(
        self,
        title: str = None,
        authors: List[TypeOrId[Author]] = None,
        artists: List[TypeOrId] = None,
        year: Year = None,
        includedTags: List[TypeOrId[Tag]] = None,
        includedTagsMode: MultiMode = None,
        excludedTags: List[TypeOrId[Tag]] = None,
        excludedTagsMode: MultiMode = None,
        status: Status = None,
        originalLanguage: LanguageCode = None,
        publicationDemographic: PublicationDemographic = None,
        ids: List[TypeOrId[Manga]] = None,
        contentRating: ContentRating = None,
        createdAtSince: datetime = None,
        updatedAtSince: datetime = None,
        order: MangaSortOrder = None,
        limit: int = 10,
        offset: int = 0,
    ):
        """
        :param title:
        :param authors:
        :param artists:
        :param year:
        :param includedTags:
        :param includedTagsMode:
        :param excludedTags:
        :param excludedTagsMode:
        :param status:
        :param originalLanguage:
        :param publicationDemographic:
        :param ids:
        :param contentRating:
        :param createdAtSince:
        :param updatedAtSince:
        :param order:
        :param limit:
        :param offset:
        """
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
    @shadows(_create)
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
        lastVolume: str = None,
        lastChapter: str = None,
        publicationDemographic: PublicationDemographic = None,
        status: Status = None,
        contentRating: ContentRating = None,
    ) -> Manga:
        ...

    def _edit(self, **kwargs):
        manga = kwargs.pop("manga")
        return self.api._make_request(
            Endpoints.Manga.EDIT, kwargs,
            urlparams={"manga": manga}
        )

    @validate_arguments
    @shadows(_edit)
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
        lastVolume: CanUnset[str] = None,
        lastChapter: CanUnset[str] = None,
        publicationDemographic: CanUnset[PublicationDemographic] = None,
        status: CanUnset[Status] = None,
        contentRating: CanUnset[ContentRating] = None,
    ) -> Manga:
        ...

    def _get_chapters(self, limit=None, offset=None, **kwargs):
        manga = kwargs.pop("manga")
        return PaginatedRequest(
            self.api, Endpoints.Manga.CHAPTERS, params=kwargs,
            urlparams={"manga": manga}, limit=limit, offset=offset,
        )

    @validate_arguments
    @shadows(_get_chapters)
    def get_chapters(
        self,
        manga: TypeOrId[Manga],
        locales: List[LanguageCode] = None,
        createdAtSince: datetime = None,
        updatedAtSince: datetime = None,
        publishAtSince: datetime = None,
        order: ChapterSortOrder = None,
        limit: int = 10,
        offset: int = 0,
    ) -> PaginatedRequest:
        ...

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
