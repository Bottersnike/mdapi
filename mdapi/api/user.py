from ..endpoints import Endpoints
from ..util import PaginatedRequest, _type_id
from ..schema import TypeOrId, User, Type
from .base import APIBase


class UserAPI(APIBase):
    def get_list(self):
        return PaginatedRequest(self.api, Endpoints.User.LIST)

    def get_list_for(self, user: TypeOrId[User]):
        return PaginatedRequest(
            self.api,
            Endpoints.User.OTHER_LIST,
            urlparams={
                "user": _type_id(user)
            }
        )

    def get_self(self) -> User:
        return Type.parse_obj(self.api._make_request(Endpoints.User.GET_ME))

    def get_followed_groups(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_GROUP)

    def get_followed_chapters(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_CHAPTERS)

    def get_followed_manga(self):
        return PaginatedRequest(self.api, Endpoints.User.FOLLOWS_MANGA)
