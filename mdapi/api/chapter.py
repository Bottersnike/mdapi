import os
from typing import BinaryIO, Generator, List, Tuple
from datetime import datetime

from pydantic.decorator import validate_arguments
import requests

from ..util import PaginatedRequest, shadows
from ..endpoints import Endpoints
from ..exceptions import (
    DownloadException, NoFollowRedirect, InvalidStatusCode, InvalidFileLength
)
from ..schema import (
    ChapterSortOrder, LanguageCode, Type, Manga, TypeOrId, Chapter,
    ScanlationGroup, User, CanUnset
)
from .base import APIBase


class ChapterAPI(APIBase):
    """
    Actions related to Managdex chapters. These actions generally relate
    to the ``/chapter`` endpoints.
    """

    def _search(self, limit=None, offset=None, **kwargs):
        return PaginatedRequest(
            self.api, Endpoints.Chapter.SEARCH, params=kwargs,
            limit=limit, offset=offset,
        )

    @validate_arguments
    @shadows(_search)
    def search(
        self,
        title: str = None,
        ids: List[TypeOrId[Chapter]] = None,
        groups: List[TypeOrId[ScanlationGroup]] = None,
        uploader: TypeOrId[User] = None,
        manga: TypeOrId[Manga] = None,
        volume: str = None,
        chapter: str = None,
        translatedLanguage: LanguageCode = None,
        createdAtSince: datetime = None,
        updatedAtSince: datetime = None,
        publishAtSince: datetime = None,
        order: ChapterSortOrder = None,
        limit: int = 10,
        offset: int = 0,
    ):
        """
        Search for a manga.

        :param title: The chapter title to search
        :param ids: A whitelist of chapter IDs to search
        :param groups: A whitelist of groups to search chapters from
        :param uploader: The chapter's uploader
        :param manga: Manga to request chapters from
        :param volume: The volume this chapter is in
        :param chapter: The chapter number
        :param translatedLanguage: The language this was translated into
        :param createdAtSince: Only show chapters created after this time
        :param updatedAtSince: Only show chapters updated after this time
        :param publishAtSince: Only show chapters publisged after this time
        :param order: The search order
        :param limit: The number of results per page
        :param offset: The offset to start from
        """
        ...

    @validate_arguments
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
            urlparams={"chapter": chapter}
        ))

    def _edit(self, **kwargs):
        chapter = kwargs.pop("chapter")
        kwargs["chapter"] = kwargs.pop("chapterNumber")
        return self.api._make_request(
            Endpoints.Chapter.EDIT, kwargs,
            urlparams={"chapter": chapter}
        )

    @validate_arguments
    @shadows(_edit)
    def edit(
        self,
        chapter: Chapter,
        title: str,
        volume: CanUnset[str] = None,
        chapterNumber: CanUnset[str] = None,
        translatedLanguage: CanUnset[LanguageCode] = None,
    ) -> Chapter:
        """
        Exit a chapter. This notably includes image
        filenames.

        :param chapter: As a this makes use of version numbers for
            conflict resolution, a `mdapi.schema.Chapter` object is
            required rather than optional.
        :param title: The new title for the chapter
        :param volume: The new volume number
        :param chapterNumber: The new chapter number
        :param translatedLanguage: This chapter's translated language
        """
        ...

    @validate_arguments
    def delete(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Delete a chapter.

        :param chapter: The chapter to delete. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.DELETE, urlparams={
            "chapter": chapter
        })

    @validate_arguments
    def mark_read(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Mark a chapter as read.

        :param chapter: The chapter to mark as read. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.MARK_READ, urlparams={
            "chapter": chapter
        })

    @validate_arguments
    def mark_unread(self, chapter: TypeOrId[Chapter]) -> None:
        """
        Mark a chapter as unread.

        :param chapter: The chapter to mark as unread. Either an
            `mdapi.schema.Chapter` object, or its UUID.
        """
        self.api._make_request(Endpoints.Chapter.MARK_UNREAD, urlparams={
            "chapter": chapter
        })

    @validate_arguments
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

    @validate_arguments
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
