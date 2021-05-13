from typing import List, Optional

from pydantic.decorator import validate_arguments

from ..util import PaginatedRequest
from ..endpoints import Endpoints
from ..schema import Type, TypeOrId, User, ScanlationGroup
from .base import APIBase


class GroupAPI(APIBase):
    @validate_arguments
    def search(
        self,
        name: str = None,
        ids: List[TypeOrId[ScanlationGroup]] = None,
        limit: int = 10,
        offset: int = 0,
    ):
        return PaginatedRequest(self.api, Endpoints.Group.SEARCH, params={
            "name": name, "ids": ids
        }, limit=limit, offset=offset)

    @validate_arguments
    def create(
        self,
        name: str,
        leader: TypeOrId[User],
        members: List[TypeOrId[User]]
    ) -> ScanlationGroup:
        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.CREATE, body={
                "name": name,
                "leader": leader,
                "members": members,
            }
        ))

    @validate_arguments
    def get(self, group: TypeOrId[ScanlationGroup]) -> ScanlationGroup:
        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.GET, urlparams={
                "group": group
            }
        ))

    @validate_arguments
    def edit(
        self,
        group: ScanlationGroup,
        name: str,
        leader: TypeOrId[User],
        members: List[TypeOrId[User]]
    ) -> ScanlationGroup:
        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.EDIT, body={
                "name": name,
                "leader": leader,
                "members": members,
                "version": group.version,
            }, urlparams={
                "group": group.id
            }
        ))

    @validate_arguments
    def delete(self, group: TypeOrId[ScanlationGroup]):
        self.api._make_request(
            Endpoints.Group.DELETE, urlparams={"group": group}
        )

    @validate_arguments
    def follow(self, group: TypeOrId[ScanlationGroup]):
        self.api._make_request(
            Endpoints.Group.FOLLOW, urlparams={"group": group}
        )

    @validate_arguments
    def unfollow(self, group: TypeOrId[ScanlationGroup]):
        self.api._make_request(
            Endpoints.Group.UNFOLLOW, urlparams={"group": group}
        )
