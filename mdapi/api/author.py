from typing import List

from pydantic.decorator import validate_arguments

from ..util import PaginatedRequest
from ..endpoints import Endpoints
from ..schema import Author, Type, TypeOrId, CanUnset
from .base import APIBase


class AuthorAPI(APIBase):
    """
    Actions related to authors. These actions generally relate to the
    ``/author`` endpoints.
    """

    @validate_arguments
    def create(self, name: str) -> Author:
        """
        Create a new author.

        :param name: The name for the author

        :returns: The newly created author
        """
        return Type.parse_obj(self.api._make_request(
            Endpoints.Author.CREATE,
            body={"name": name}
        ))

    @validate_arguments
    def get(self, author: TypeOrId[Author]) -> Author:
        """
        Request full details for an author.

        :param author: The author to lookup. Either an
            `mdapi.schema.Author` object, or their UUID.

        :returns: The author, if found
        """
        return Type.parse_obj(self.api._make_request(
            Endpoints.Author.GET,
            urlparams={"author": author}
        ))

    @validate_arguments
    def search(
        self,
        name: str = None,
        ids: List[TypeOrId[Author]] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> PaginatedRequest[Author]:
        """
        Search for an author by name.

        :param name: The name to search with
        :param ids: Whitelist of authors to search from
        :param limit: The number of results per page
        :param offset: The offset to start from

        :returns: Paginated search results
        """
        return PaginatedRequest(self.api, Endpoints.Author.SEARCH, params={
            "name": name, "ids": ids
        }, limit=limit, offset=offset)

    @validate_arguments
    def edit(
        self, author: TypeOrId[Author], name: CanUnset[str] = None
    ) -> None:
        """
        Make edits to a user. Currently only changing the author name is
        supported.

        :param author: The author to edit. Either an
            `mdapi.schema.Author` object, or their UUID.
        :param name: The new name for the author
        """

        body = {"version": author.version}
        if name is not None:
            body["name"] = name
        self.api._make_request(
            Endpoints.Author.EDIT, body=body, urlparams={"author": author.id}
        )

    @validate_arguments
    def delete(self, author: TypeOrId[Author]) -> None:
        """
        Delete an author.

        :param author: The author to delete. Either an
            `mdapi.schema.Author` object, or their UUID.
        """
        self.api._make_request(
            Endpoints.Author.delete, urlparams={"author": author}
        )
