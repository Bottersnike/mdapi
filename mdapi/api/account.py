from ..endpoints import Endpoints
from ..schema import Type
from .base import APIBase


class AccountAPI(APIBase):
    def create(self, username, password, email):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Account.CREATE, body={
                "username": username,
                "password": password,
                "email": email
            }
        ))

    def recover(self, code):
        self.api._make_request(Endpoints.Account.RECOVER)

    def complete_recover(self, code, password):
        self.api._make_request(Endpoints.Account.COMPLETE_RECOVER, body={
            "newPassword": password
        }, urlparams={
            "code": code
        })

    def activate(self, code):
        self.api._make_request(Endpoints.Account.ACTIVATE, urlparams={
            "code": code
        })

    def activate_resend(self, email):
        self.api._make_request(Endpoints.Account.ACTIVATE_RESEND, body={
            "email": email
        })
