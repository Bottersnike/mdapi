from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Type


class AuthorAPI:
    def __init__(self, api):
        self.api = api

    def create(self, name):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Author.CREATE,
            body={"name": name}
        ))

    def get(self, author):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Author.GET,
            urlparams={"author": _type_id(author)}
        ))

    def search(self, limit=10, offset=0, name=None):
        return PaginatedRequest(self.api, Endpoints.Author.SEARCH, params={
            "limit": limit, "offset": offset, "name": name
        })

    def edit(self, author, name=None):
        body = {"version": author.version}
        if name is not None:
            body["name"] = name
        self.api._make_request(
            Endpoints.Author.EDIT, body=body, urlparams={"author": author.id}
        )

    def delete(self, author):
        self.api._make_request(
            Endpoints.Author.delete, urlparams={"author": _type_id(author)}
        )
