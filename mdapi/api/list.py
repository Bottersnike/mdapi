from typing import List

from pydantic import validate_arguments

from ..util import PaginatedRequest
from ..endpoints import Endpoints
from ..schema import TypeOrId, Type, CustomListVisibility, Manga, CustomList
from .base import APIBase


class ListAPI(APIBase):
    @validate_arguments
    def create(
        self,
        name: str,
        visibility: CustomListVisibility,
        manga: List[TypeOrId[Manga]]
    ) -> CustomList:
        return Type.parse_obj(self.api._make_request(
            Endpoints.List.CREATE,
            body={
                "name": name,
                "visibility": visibility,
                "manga": manga,
                "version": 1,
            }
        ))

    @validate_arguments
    def edit(
        self,
        custom_list: CustomList,
        name: str,
        visibility: CustomListVisibility,
        manga: List[TypeOrId[Manga]]
    ):
        self.api._make_request(
            Endpoints.List.EDIT, body={
                "name": name,
                "visibility": visibility,
                "manga": manga,
                "version": custom_list.version,
            }, urlparams={"list": custom_list.id}
        )

    @validate_arguments
    def get(self, list_id: TypeOrId[CustomList]) -> CustomList:
        return Type.parse_obj(self.api._make_request(
            Endpoints.List.GET, urlparams={
                "list": list_id
            }
        ))

    @validate_arguments
    def delete(self, list_id: TypeOrId[CustomList]) -> None:
        self.api._make_request(
            Endpoints.List.DELETE, urlparams={
                "list": list_id
            }
        )

    @validate_arguments
    def get_feed(
        self,
        list_id: TypeOrId[CustomList],
        limit: int = 10,
        offset: int = 0,
    ):
        return PaginatedRequest(
            self.api,
            Endpoints.List.GET_FEED,
            urlparams={"list": list_id},
            limit=limit, offset=offset
        )
