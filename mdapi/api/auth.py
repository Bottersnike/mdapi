from ..endpoints import Endpoints
from ..exceptions import MdException
from .base import APIBase


class AuthAPI(APIBase):
    def login(self, username, password):
        try:
            token = self.api._make_request(Endpoints.Auth.LOGIN, {
                "username": username,
                "password": password
            }).get("token")
        except MdException:
            raise

        self.api._authenticate(username, token)

    def check(self):
        return self.api._make_request(Endpoints.Auth.CHECK)

    def logout(self):
        self.api._make_request(Endpoints.Auth.LOGOUT)
        self.api._authenticate(None, None)

    def refresh(self):
        ref = self.api._get_refresh_token()
        if ref is None:
            raise MdException("Not logged in")

        try:
            token = self.api._make_request(
                Endpoints.Auth.REFRESH, {"token": ref}
            ).get("token")
        except MdException:
            raise

        self.api._authenticate(None, token)
