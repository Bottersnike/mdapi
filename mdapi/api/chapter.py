from build.lib.mdapi.schema import Chapter, ScanlationGroup, User
import os
from typing import BinaryIO, Generator, List, Tuple

import requests

from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..exceptions import (
    DownloadException, NoFollowRedirect, InvalidStatusCode, InvalidFileLength
)
from ..schema import ChaptersListOrder, LanguageCode, Type, Manga, TypeOrId
from .base import APIBase


class ChapterAPI(APIBase):
    """
    Actions related to Managdex chapters. These actions generally relate
    to the ``/chapter`` endpoints.
    """

    def search(
        self,
        manga: TypeOrId[Manga] = None,
        limit: int = 10, offset: int = 0,
        uploader: TypeOrId[User] = None,
        volume: str = None,
        chapter: str = None,
        translated_language: List[LanguageCode] = None,
        ids: List[TypeOrId[Manga]] = None,
        groups: List[TypeOrId[ScanlationGroup]] = None,
        created_at_since: str = None,
        updated_at_since: str = None,
        publish_at_since: str = None,
        order: ChaptersListOrder = None,
    ):
        """
        Search for a manga.

        :param manga: Manga to request chapters from
        :param uploader: The chapter's uploader
        :param volume: The volume this chapter is in
        :param chapter: The chapter number
        :param translated_language: The language this was translated into
        :param ids: A whitelist of chapter IDs to search
        :param groups: A whitelist of groups to search chapters from
        :param created_at_since: Only show chapters created after this time
        :param updated_at_since: Only show chapters updated after this time
        :param publish_at_since: Only show chapters publisged after this time
        :param order: The search order
        :param limit: The number of results per page
        :param offset: The offset to start from
        """

        return PaginatedRequest(self.api, Endpoints.Chapter.SEARCH, params={
            "limit": limit, "offset": offset,
            "uploader": _type_id(uploader),
            "manga": _type_id(manga), "volume": volume, "chapter": chapter,
            "translatedLanguage": translated_language,
            "ids": [_type_id(i) for i in ids or []] or None,
            "groups": [_type_id(i) for i in groups or []] or None,
            "createdAtSince": created_at_since,
            "updatedAtSince": updated_at_since,
            "publishAtSince": publish_at_since,
            **(order.serialize() if order else {})
        })

    def get(self, chapter: TypeOrId[Chapter]) -> Chapter:
        """
        Request full details for an chapter. This notably includes image
        filenames.

        :param chapter: The author to lookup. Either an
            `mdapi.schema.Chapter` object, or its UUID.

        :returns: The chapter, if found
        """
        return Type.parse_obj(self.api._make_request(
            Endpoints.Chapter.GET,
            urlparams={"chapter": _type_id(chapter)}
        ))

    def edit(
        self,
        chapter: Chapter,
        title: str,
        data: List[str],
        data_saver: List[str],
        volume: str = None,
        chapter_number: str = None,
        translated_language: LanguageCode = None,
    ) -> Chapter:
        """
        Exit a chapter. This notably includes image
        filenames.

        :param chapter: As a this makes use of version numbers for
            conflict resolution, a `mdapi.schema.Chapter` object is
            required rather than optional.
        :param title: The new title for the chapter
        :param data: The new array of page URLs
        :param data_saver: The new array of data-saver page URLs
        :param volume: The new volume number
        :param chapter_number: The new chapter number
        :param translated_language: This chapter's translated language
        """
        Type.parse_obj(self.api._make_request(
            Endpoints.Chapter.EDIT,
            urlparams={
                "chapter": chapter.id
            }, body={
                "title": title,
                "data": data,
                "data_saver": data_saver,
                "volume": volume,
                "chapter": chapter_number,
                "translatedLanguage": translated_language,
                "version": chapter.version
            }
        ))

    def delete(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Delete a chapter.

        :param chapter: The chapter to delete. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.DELETE, urlparams={
            "chapter": _type_id(chapter)
        })

    def mark_read(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Mark a chapter as read.

        :param chapter: The chapter to mark as read. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.MARK_READ, urlparams={
            "chapter": _type_id(chapter)
        })

    def mark_unread(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Mark a chapter as unread.

        :param chapter: The chapter to mark as unread. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.MARK_UNREAD, urlparams={
            "chapter": _type_id(chapter)
        })

    def page_urls_for(
        self, chapter: Chapter, data_saver: bool = False
    ) -> Generator[str, None, None]:
        """
        Get a list of all page image URLs for this chapter.

        .. note::
            If the ``MD_CHAPTER_BASE_URL`` environment variable is set,
            the API is not queried for an MD@H server, and the set value
            is instead used. This could be useful when testing MD@H
            clients.

        :param chater: The chapter to get the pages for
        :param data_saver: Should data-saver URLs be provided instead?

        :returns: A generator that produces page URLs
        """
        # Manual override for testing
        if "MD_CHAPTER_BASE_URL" in os.environ:
            base = os.environ.get("MD_CHAPTER_BASE_URL")
        else:
            base = self.api.md.misc.get_md_at_home_url(chapter)

        base += "/data-saver/" if data_saver else "/data/"
        base += chapter.hash + "/"

        for i in chapter.dataSaver if data_saver else chapter.data:
            yield base + i

    def download_page(
        self, url: str, follow_redirect: bool = False, report_mdah: bool = True
    ) -> Generator[Tuple[bytes, int], None, None]:
        """
        Download a single page of a manga.

        :param url: The URL for the page
        :param follow_redirect: Should redirects be followed?
        :param report_mdah: Report node statistics to MD@H.

        .. note::
            Unless there is a good reason, it is recommended to always
            leave ``report_mdah`` set to ``True``, to ensure faulty
            nodes are accurately monitored.

        :returns: A generator that yields ``(chunk, total_length)``.
        """
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
        self,
        url: str, output: BinaryIO, follow_redirect: bool = False,
        is_iter: bool = False, report_mdah: bool = True
    ) -> Generator[Tuple[int, int], None, None]:
        """
        Download a page into a file-like. Paramaters are mostly the same
        as `mdapi.chapter.Chapter.download_page`.

        :param url: The URL for the page
        :param output: The output file-like to save to
        :param follow_redirect: Should redirects be followed?
        :param is_iter: Should this function return a generator?
        :param report_mdah: Report node statistics to MD@H.

        :returns: A generator yielding ``(downloaded, total_length)`` if
            ``is_iter`` is ``True``.
        """
        downloaded = 0
        for chunk, total_length in (
            self.download_page(url, follow_redirect, report_mdah)
        ):
            downloaded += len(chunk)
            output.write(chunk)
            if is_iter:
                yield (downloaded, total_length)
