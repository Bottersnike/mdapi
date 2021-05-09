from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Type
from .base import APIBase


class ListAPI(APIBase):
    def create(self, name, visibility, manga):
        return Type.parse_obj(self.api._make_request(
            Endpoints.List.CREATE,
            body={
                "name": name,
                "visibility": visibility,
                "manga": [_type_id(i) for i in manga]
            }
        ))

    def edit(self, list, name=None, visibility=None, manga=None):
        body = {"version": list}
        if name is not None:
            body["name"] = name
        if visibility is not None:
            body["visibility"] = visibility
        if manga is not None:
            body["manga"] = [_type_id(i) for i in manga]

        self.api._make_request(
            Endpoints.List.EDIT, body=body, urlparams={"list": list.id}
        )

    def get(self, list):
        return Type.parse_obj(self.api._make_request(
            Endpoints.List.GET, urlparams={
                "list": _type_id(list)
            }
        ))

    def delete(self, list):
        self.api._make_request(
            Endpoints.List.DELETE, urlparams={
                "list": _type_id(list)
            }
        )

    def get_feed(self, list):
        return PaginatedRequest(
            self.api,
            Endpoints.List.GET_FEED, urlparams={
                "list": _type_id(list)
            }
        )
