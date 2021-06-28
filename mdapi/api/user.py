from pydantic.decorator import validate_arguments

from ..endpoints import Endpoints
from ..util import PaginatedRequest
from ..schema import TypeOrId, User, Type
from .base import APIBase


class UserAPI(APIBase):
    @validate_arguments
    def get_list(self, limit: int = 10, offset: int = 0):
        return PaginatedRequest(
            self.api, Endpoints.User.LIST, limit=limit, offset=offset
        )

    @validate_arguments
    def get_list_for(
        self, user: TypeOrId[User], limit: int = 10, offset: int = 0
    ):
        return PaginatedRequest(
            self.api,
            Endpoints.User.OTHER_LIST,
            urlparams={
                "user": user
            },
            limit=limit, offset=offset
        )

    def get_self(self) -> User:
        return Type.parse_obj(self.api._make_request(Endpoints.User.GET_ME))

    @validate_arguments
    def get_followed_groups(self, limit: int = 10, offset: int = 0):
        return PaginatedRequest(
            self.api, Endpoints.User.FOLLOWS_GROUP, limit=limit, offset=offset
        )

    @validate_arguments
    def get_followed_chapters(self, limit: int = 10, offset: int = 0):
        return PaginatedRequest(
            self.api, Endpoints.User.FOLLOWS_CHAPTERS,
            limit=limit, offset=offset
        )

    @validate_arguments
    def get_followed_manga(self, limit: int = 10, offset: int = 0):
        return PaginatedRequest(
            self.api, Endpoints.User.FOLLOWS_MANGA, limit=limit, offset=offset
        )
