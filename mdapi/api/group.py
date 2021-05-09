from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Type
from .base import APIBase


class GroupAPI(APIBase):
    def search(self, limit=10, offset=0, name=None):
        return PaginatedRequest(self.api, Endpoints.Group.SEARCH, params={
            "limit": limit, "offset": offset, "name": name
        })

    def create(self, name, leader, members):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.CREATE, body={
                "name": name,
                "leader": _type_id(leader),
                "members": [_type_id(i) for i in members]
            }
        ))

    def get(self, group):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.GET, urlparams={
                "group": _type_id(group)
            }
        ))

    def edit(self, group, name=None, leader=None, members=None):
        body = {"version": group.version}
        if name is not None:
            body["name"] = name
        if leader is not None:
            body["leader"] = _type_id(leader)
        if members is not None:
            body["members"] = [_type_id(i) for i in members]

        return Type.parse_obj(self.api._make_request(
            Endpoints.Group.EDIT, body=body, urlparams={
                "group": group.id
            }
        ))

    def delete(self, group):
        self.api._make_request(
            Endpoints.Group.DELETE, urlparams={
                "group": _type_id(group)
            }
        )

    def follow(self, group):
        self.api._make_request(
            Endpoints.Group.FOLLOW, urlparams={
                "group": _type_id(group)
            }
        )

    def unfollow(self, group):
        self.api._make_request(
            Endpoints.Group.UNFOLLOW, urlparams={
                "group": _type_id(group)
            }
        )
