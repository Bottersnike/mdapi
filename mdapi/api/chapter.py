import os

import requests

from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..exceptions import (
    DownloadException, NoFollowRedirect, InvalidStatusCode, InvalidFileLength
)
from ..schema import Type
from .base import APIBase


class ChapterAPI(APIBase):
    def search(
        self, manga=None,
        limit=10, offset=0, uploader=None, volume=None,
        chapter=None, translatedLanguage=None
    ):
        return PaginatedRequest(self.api, Endpoints.Chapter.SEARCH, params={
                "limit": limit, "offset": offset, "uploader": uploader,
                "manga": _type_id(manga), "volume": volume, "chapter": chapter,
                "translatedLanguage": translatedLanguage
            })

    def get(self, chapter):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Chapter.GET,
            urlparams={"chapter": _type_id(chapter)}
        ))

    def edit(self, chapter):
        self.api._make_request(Endpoints.Chapter.EDIT, urlparams={
            "chapter": _type_id(chapter)
        })

    def delete(self, chapter):
        self.api._make_request(Endpoints.Chapter.DELETE, urlparams={
            "chapter": _type_id(chapter)
        })

    def mark_read(self, chapter):
        self.api._make_request(Endpoints.Chapter.MARK_READ, urlparams={
            "chapter": _type_id(chapter)
        })

    def mark_unread(self, chapter):
        self.api._make_request(Endpoints.Chapter.MARK_UNREAD, urlparams={
            "chapter": _type_id(chapter)
        })

    def page_urls_for(self, chapter, data_saver=False):
        # Manual override for testing
        if "MD_CHAPTER_BASE_URL" in os.environ:
            base = os.environ.get("MD_CHAPTER_BASE_URL")
        else:
            base = self.api.md.misc.get_md_at_home_url(chapter)

        base += "/data-saver/" if data_saver else "/data/"
        base += chapter.hash + "/"

        for i in chapter.dataSaver if data_saver else chapter.data:
            yield base + i

    def download_page(self, url, follow_redirect=False, report_mdah=True):
        try:
            req = requests.get(url, stream=True)
        except requests.RequestException:
            if report_mdah:
                self.md.misc.report_mdah(url, False, False, 0, 0)
            raise DownloadException

        if req.url != url and not follow_redirect:
            if report_mdah:
                self.md.misc.report_mdah(
                    url, False, False, 0, req.elapsed.microseconds // 1000
                )
            raise NoFollowRedirect(req.url)

        if req.status_code != 200:
            if report_mdah:
                self.md.misc.report_mdah(
                    url, False, False, 0, req.elapsed.microseconds // 1000
                )

            raise InvalidStatusCode(req.status_code)

        is_cached = req.headers.get("X-Cache", "").startswith("HIT")
        total_length = int(req.headers.get("Content-Length"))

        if not total_length:
            if report_mdah:
                self.md.misc.report_mdah(
                    url, False, is_cached, 0, req.elapsed.microseconds // 1000
                )

            raise InvalidFileLength(total_length)

        chunk_size = 131072  # 0.125 MB
        bytes_downloaded = 0

        try:
            for chunk in req.iter_content(chunk_size=chunk_size):
                bytes_downloaded += len(chunk)
                yield (chunk, total_length)
        except requests.RequestException:
            if report_mdah:
                self.md.misc.report_mdah(
                    url, False, is_cached, bytes_downloaded,
                    req.elapsed.microseconds // 1000
                )
            raise DownloadException()

        if report_mdah:
            self.md.misc.report_mdah(
                url, True, is_cached, bytes_downloaded,
                req.elapsed.microseconds // 1000
            )

    def download_page_to(
        self, url, output, follow_redirect=False, is_iter=False,
        report_mdah=True
    ):
        downloaded = 0
        for chunk, total_length in (
            self.download_page(url, follow_redirect, report_mdah)
        ):
            downloaded += len(chunk)
            output.write(chunk)
            if is_iter:
                yield (downloaded, total_length)
