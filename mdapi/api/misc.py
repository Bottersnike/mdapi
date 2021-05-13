from typing import List
from pydantic import validate_arguments

from ..endpoints import Endpoints
from ..schema import TypeOrId, Chapter, LegacyType, MappingID, Type
from .base import APIBase


class MiscAPI(APIBase):
    @validate_arguments
    def get_md_at_home_url(
        self, chapter: TypeOrId[Chapter], force_port_443: bool = False
    ):
        return self.api._make_request(Endpoints.GET_MD_AT_HOME, urlparams={
            "chapter": chapter
        }, params={
            "forcePort443": True if force_port_443 else None
        })["baseUrl"]

    @validate_arguments
    def solve_captcha(self, challenge: str):
        self.api._make_request(Endpoints.SOLVE_CAPTCHA, body={
            "captchaChallenge": challenge
        })

    @validate_arguments
    def legacy_mapping(
        self, manga_ids: List[int], type: LegacyType = "manga"
    ) -> List[MappingID]:
        return [
            Type.parse_obj(i.get("data", i))
            for i in self.api._make_request(Endpoints.LEGACY_MAPPING, body={
                "type": type,
                "ids": manga_ids
            })
        ]

    @validate_arguments
    def report_mdah(
        self, url: str, success: bool, cached: bool, num_bytes: int,
        duration: int
    ):
        self.api._make_request(Endpoints.MDAH_REPORT, body={
            "url": url, "success": success, "cached": cached,
            "bytes": num_bytes, "duration": duration
        })
