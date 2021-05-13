from ..endpoints import Endpoints
from ..schema import Type, User
from .base import APIBase


class AccountAPI(APIBase):
    """
    Actions related to Managdex accounts. These actions generally relate
    to the ``/account`` endpoints.
    """

    def create(self, username: str, password: str, email: str) -> User:
        """
        Create a new Mangadex account.

        :param username: New account's username
        :param password: New account's password
        :param email: New account's email

        :returns: The newly created user
        """
        return Type.parse_obj(self.api._make_request(
            Endpoints.Account.CREATE, body={
                "username": username,
                "password": password,
                "email": email
            }
        ))

    def recover(self, email: str) -> None:
        """
        Begin an account recovery. This will send an email to ``email``
        if an account exists with that email address.

        :param email: The account's email address
        """
        self.api._make_request(Endpoints.Account.RECOVER, body={
            "email": email
        })

    def complete_recover(self, code: str, password: str) -> None:
        """
        Complete an account recovery.

        :param code: The code received via email
        :param password: The new password to change to
        """
        self.api._make_request(Endpoints.Account.COMPLETE_RECOVER, body={
            "newPassword": password
        }, urlparams={
            "code": code
        })

    def activate(self, code: str) -> None:
        """
        Activate a new Mangadex account.

        :param code: The code received via email
        """
        self.api._make_request(Endpoints.Account.ACTIVATE, urlparams={
            "code": code
        })

    def activate_resend(self, email: str) -> None:
        """
        Request a new email be sent during the account activate process.

        :param email: The new user's email address
        """
        self.api._make_request(Endpoints.Account.ACTIVATE_RESEND, body={
            "email": email
        })
