import functools
from mdapi.schema.const import SortOrder
from mdapi.schema.search import ChapterSortOrder
import os

import click

from .mdapi import MdAPI, MdException, NotLoggedIn


def sanitize(x):
    return "".join(i for i in x if (i.isalnum() or i in "._- "))


def uses_md(func):
    @click.option("--debug", is_flag=True)
    @functools.wraps(func)
    def wrapper(debug, *args, **kwargs):
        MdAPI.DEBUG = debug
        md = MdAPI()
        return func(md, *args, **kwargs)
    return wrapper


@click.group()
def cli():
    pass


@cli.command()
@uses_md
def login(md: MdAPI):
    if md.user is not None:
        if not click.confirm(
            "You are already logged in. "
            "Would you like to login to a different account?"
        ):
            return
        md.auth.logout()

    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    try:
        md.auth.login(username, password)
    except NotLoggedIn:
        click.echo(click.style("Username or password incorrect!", fg="red"))
    except MdException:
        click.echo(click.style("Failed to login.", fg="red"))
    else:
        click.echo(click.style(f"Logged in as {username}", fg="green"))


@cli.command()
@uses_md
def logout(md: MdAPI):
    if md.user is None:
        click.echo(click.style("You are not logged in", fg="red"))
    else:
        md.auth.logout()


@cli.command()
@uses_md
def whoami(md: MdAPI):
    try:
        user = md.user.get_self()
    except NotLoggedIn:
        click.echo(click.style("Not logged in", fg="red"))
        return

    click.echo(user.username)


@cli.command()
@uses_md
@click.argument("query", nargs=-1)
def search(md: MdAPI, query):
    results = md.manga.search(title=" ".join(query))
    results._ensure_populated()

    click.echo(click.style(f" -=- {results.total} results -=-", fg="green"))

    while (page := results.next_page()):
        for i in page:
            click.echo(click.style(i.id, fg="magenta"), nl=False)
            click.echo(" ", nl=False)
            click.echo(click.style(str(i.title), fg="bright_blue"))
        if not results.has_more:
            break
        if not click.confirm("Show more?"):
            break


@cli.command()
@uses_md
@click.argument("manga", nargs=1)
@click.option("-l", "--locales", default="en")
def chapters(md: MdAPI, manga, locales):
    results = md.manga.get_chapters(
        manga, locales=locales.split(","),
        order=ChapterSortOrder(chapter=SortOrder.desc)
    )
    results._ensure_populated()

    click.echo(click.style(f" -=- {results.total} chapters -=-", fg="green"))

    while (page := results.next_page()):
        for i in page:
            click.echo(click.style(i.id, fg="magenta"), nl=False)
            click.echo(" ", nl=False)
            click.echo(
                click.style(f"({i.chapter}) ", fg="bright_blue"), nl=False
            )
            if i.title:
                click.echo(click.style(str(i.title), fg="blue"), nl=False)
            click.echo("")
        if not results.has_more:
            break
        if not click.confirm("Show more?"):
            break


def download_chapter(md: MdAPI, chapter, path):
    for n, page in enumerate(md.chapter.page_urls_for(chapter)):
        ext = page.split(".")[-1]
        filename = f"{n + 1:03}.{ext}"
        with open(os.path.join(path, filename), "wb") as f:
            with click.progressbar(label=filename, length=1) as bar:
                bar.update(0)
                for downloaded, total_length in (
                    md.chapter.download_page_to(page, f, is_iter=True)
                ):
                    bar.pos = downloaded / total_length
                    bar.update(0)
                bar.pos = 1
                bar.update(0)


def read_manga(manga, locales="en"):
    md = MdAPI()
    manga = md.manga.get(manga)
    results = md.manga.get_chapters(manga.id, locales=locales)
    results._ensure_populated()
    if not click.confirm(
        f"This will download {results.total} chapters. Proceed?"
    ):
        return

    for chapter in results:
        click.echo(
            click.style(f"Downloading chapter {chapter.chapter}", fg="green")
        )
        path = (
            f"Manga/{sanitize(str(manga.title) or 'No title')}/"
            f"{chapter.translatedLanguage}-{chapter.chapter}/"
        )
        click.echo(click.style(f"Downloading to {path}", fg="green"))
        os.makedirs(path, exist_ok=True)
        download_chapter(md, chapter, path)


@cli.command()
@uses_md
@click.argument("chapter", nargs=1)
@click.option("-l", "--locales", default="en")
def read(md: MdAPI, chapter, locales):
    chapter_ = md.chapter.get(chapter)
    if chapter_ is None:
        return read_manga(chapter, locales)
    chapter = chapter_

    manga = None

    for i in chapter.relationships:
        if i.type == "manga":
            manga = md.manga.get(i.id)
            break
    else:
        click.echo(click.style("Failed to locate parent manga", fg="red"))
        return

    path = (
        f"Manga/{sanitize(str(manga.title) or 'No title')}/{chapter.chapter}/"
    )
    click.echo(click.style(f"Downloading to {path}", fg="green"))
    os.makedirs(path, exist_ok=True)

    download_chapter(md, chapter, path)


def main():
    cli()
