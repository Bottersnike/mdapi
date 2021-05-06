import os

import requests
import click

from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Type


class ChapterAPI:
    def __init__(self, api):
        self.api = api

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

    def download(self, chapter, path):
        # base = self.get_md_at_home_url(chapter)
        base = "https://reh3tgm2rs8sr.xnvda7fch4zhr.mangadex.network//"

        for i in chapter.data:
            url = f"{base}data/{chapter.hash}/{i}"
            req = requests.get(url, stream=True)
            if req.url != url:
                click.echo(click.style(
                    f"Refusing to follow redirect to {req.url}", fg="red"
                ))
                return
            if req.status_code != 200:
                click.echo(click.style(
                    f"Invalid status code: {req.status_code}", fg="red"
                ))
                continue
            total_length = int(req.headers.get('content-length'))
            if not total_length:
                click.echo(click.style(
                    "Failed to get file length", fg="red"
                ))
                continue

            with open(os.path.join(path, i), "wb") as f:
                with click.progressbar(label=i, length=total_length) as bar:
                    size = f.write(req.content)
                    bar.update(size)
