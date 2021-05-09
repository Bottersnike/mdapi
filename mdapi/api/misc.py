from ..util import _type_id
from ..endpoints import Endpoints
from ..schema import Type


class MiscAPI:
    def __init__(self, api):
        self.api = api

    def get_md_at_home_url(self, chapter, force_port_443=False):
        return self.api._make_request(Endpoints.GET_MD_AT_HOME, urlparams={
            "chapter": _type_id(chapter)
        }, params={
            "forcePort443": True if force_port_443 else None
        })["baseUrl"]

    def solve_captcha(self, challenge):
        self.api._make_request(Endpoints.SOLVE_CAPTCHA, body={
            "captchaChallenge": challenge
        })

    def legacy_mapping(self, manga_ids, type="manga"):
        return [
            Type.parse_obj(i.get("data", i))
            for i in self.api._make_request(Endpoints.LEGACY_MAPPING, body={
                "type": type,
                "ids": manga_ids
            })
        ]
