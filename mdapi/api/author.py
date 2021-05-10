from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Author, Type, TypeOrId
from .base import APIBase


class AuthorAPI(APIBase):
    """
    Actions related to authors. These actions generally relate to the
    ``/author`` endpoints.
    """

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

    def get(self, author: TypeOrId[Author]) -> Author:
        """
        Request full details for an author.

        :param author: The author to lookup. Either an
            `mdapi.schema.Author` object, or their UUID.

        :returns: The author, if found
        """
        return Type.parse_obj(self.api._make_request(
            Endpoints.Author.GET,
            urlparams={"author": _type_id(author)}
        ))

    def search(
        self, limit: int = 10, offset: int = 0, name: str = None
    ) -> PaginatedRequest[Author]:
        """
        Search for an author by name.

        :param name: The name to search with
        :param limit: The number of results per page
        :param offset: The offset to start from

        :returns: Paginated search results
        """
        return PaginatedRequest(self.api, Endpoints.Author.SEARCH, params={
            "limit": limit, "offset": offset, "name": name
        })

    def edit(
        self, author: TypeOrId[Author], name: str = None
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

    def delete(self, author: TypeOrId[Author]) -> None:
        """
        Delete an author.

        :param author: The author to delete. Either an
            `mdapi.schema.Author` object, or their UUID.
        """
        self.api._make_request(
            Endpoints.Author.delete, urlparams={"author": _type_id(author)}
        )
