from ..util import _type_id
from ..endpoints import Endpoints
from ..schema import Type


class MiscAPI:
    def __init__(self, api):
        self.api = api

    def get_md_at_home_url(self, chapter):
        return self._make_request(Endpoints.GET_MD_AT_HOME, urlparams={
            "chapter": _type_id(chapter)
        })

    def solve_captcha(self, challenge):
        self._make_request(Endpoints.SOLVE_CAPTCHA, body={
            "captchaChallenge": challenge
        })

    def legacy_mapping(self, manga_ids, type="manga"):
        return [
            Type.parse_obj(i.get("data", i))
            for i in self._make_request(Endpoints.LEGACY_MAPPING, body={
                "type": type,
                "ids": manga_ids
            })
        ]