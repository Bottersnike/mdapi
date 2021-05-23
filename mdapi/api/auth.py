from pydantic.decorator import validate_arguments

from ..endpoints import Endpoints
from ..exceptions import MdException
from .base import APIBase


class AuthAPI(APIBase):
    """
    Actions related to Managdex authentication. The seperation between
    these actions and :mod:`mdapi.api.account` are to remain in-line
    with the structure of the upstream API. These actions generally
    relate to the ``/account`` endpoints.
    """

    @validate_arguments
    def login(self, username: str, password: str) -> None:
        """
        Login to a Mangadex account

        :param username: Account's username
        :param password: Account's password
        """
        try:
            token = self.api._make_request(Endpoints.Auth.LOGIN, {
                "username": username,
                "password": password
            }).get("token")
        except MdException:
            raise

        self.api._authenticate(username, token)

    def check(self) -> bool:
        """
        Check if a user is currently logged in

        :returns: If a user is currently logged in
        """
        return self.api._make_request(Endpoints.Auth.CHECK)

    def logout(self) -> None:
        """
        Logout the current user. If no user is logged in, this will
        still make a logout request, but it will have no effect.
        """
        try:
            self.api._make_request(Endpoints.Auth.LOGOUT)
        except MdException:
            pass
        self.api._authenticate(None, None)

    def refresh(self) -> None:
        """
        Refresh the current session token using the refresh token.
        """
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
