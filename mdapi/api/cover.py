from typing import List, BinaryIO

from pydantic.decorator import validate_arguments

from ..util import PaginatedRequest
from ..endpoints import Endpoints
from ..schema import (
    Author, TypeOrId, CanUnset, CoverSortOrder, Cover, Manga, User, Type
)
from .base import APIBase


class CoverAPI(APIBase):
    @validate_arguments
    def search(
        self,
        manga: List[TypeOrId[Manga]] = None,
        ids: List[TypeOrId[Cover]] = None,
        uploaders: List[TypeOrId[User]] = None,
        order: CoverSortOrder = None,
        limit: int = 10,
        offset: int = 0,
    ) -> PaginatedRequest[Cover]:
        return PaginatedRequest(self.api, Endpoints.Cover.SEARCH, params={
            "manga": manga, "ids": ids, "uploaders": uploaders, "order": order
        }, limit=limit, offset=offset)

    def upload(
        self, manga: TypeOrId[Manga], file_: BinaryIO
    ) -> Cover:
        manga = TypeOrId.return_type(manga)
        return Type.parse_obj(self.api._make_request(
            Endpoints.Cover.UPLOAD, urlparams={"manga": manga},
            files={"file": file_}
        ))

    @validate_arguments
    def edit(
        self, cover: Cover, volume: CanUnset[str] = None,
        description: CanUnset[str] = None
    ) -> Cover:
        body = {"version": cover.version}
        if volume is not None:
            body["volume"] = volume
        if description is not None:
            body["description"] = volume
        return Type.parse_obj(self.api._make_request(
            Endpoints.Cover.EDIT, body=body, urlparams={"cover": cover.id}
        ))

    @validate_arguments
    def delete(self, cover: TypeOrId[Author]) -> None:
        self.api._make_request(
            Endpoints.Cover.DELETE, urlparams={"cover": cover}
        )
