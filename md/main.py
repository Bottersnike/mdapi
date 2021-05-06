import os
from devtools import debug
import click

from .mdapi import MdAPI, MdException
from .schema_new import EditManga, NewManga
from .schema import LocalizedString


def sanitize(x):
    return "".join(i for i in x if (i.isalnum() or i in "._- "))


@click.group()
def cli():
    pass


@cli.command()
def login():
    md = MdAPI()

    if md.user is not None:
        if not click.confirm(
            "You are already logged in. "
            "Would you like to login to a different account?"
        ):
            return
        md.logout()

    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    try:
        md.login(username, password)
    except MdException:
        click.echo(click.style("Username or password incorrect!", fg="red"))
    else:
        click.echo(click.style(f"Logged in as {username}", fg="green"))


@cli.command()
def logout():
    md = MdAPI()

    if md.user is None:
        click.echo(click.style("You are not logged in", fg="red"))
    else:
        md.logout()


@cli.command()
def whoami():
    md = MdAPI()

    user = md.get_user()

    click.echo(user.username)


@cli.command()
@click.argument("query", nargs=-1)
def search(query):
    md = MdAPI()
    results = md.manga.search(title=" ".join(query))
    results._ensure_populated()

    click.echo(click.style(f" -=- {results.total} results -=-", fg="green"))

    while (page := results.next_page()):
        for i in page:
            click.echo(click.style(i.id, fg="magenta"), nl=False)
            click.echo(" ", nl=False)
            click.echo(click.style(str(i.title), fg="bright_blue"))
        # click.echo("---")
        # click.echo(i.description)
        if not click.confirm("Show more?"):
            break


@cli.command()
@click.argument("manga", nargs=1)
def chapters(manga):
    md = MdAPI()
    results = md.get_chapters(manga)
    results._ensure_populated()

    click.echo(click.style(f" -=- {results.total} chapters -=-", fg="green"))

    while (page := results.next_page()):
        for i in page:
            click.echo(click.style(i.id, fg="magenta"), nl=False)
            click.echo(" ", nl=False)
            click.echo(click.style(f"({i.chapter}) ", fg="bright_blue"), nl=False)
            if i.title:
                click.echo(click.style(str(i.title), fg="blue"), nl=False)
            click.echo("")
        # click.echo("---")
        # click.echo(i.description)
        if not click.confirm("Show more?"):
            break


@cli.command()
@click.argument("chapter", nargs=1)
def read(chapter):
    md = MdAPI()
    chapter = md.get_chapter(chapter)
    manga = None

    for i in chapter.relationships:
        if i.type == "manga":
            manga = md.get_manga(i.id)
            break
    else:
        click.echo(click.style("Failed to locate parent manga", fg="red"))
        return

    path = f"Manga/{sanitize(str(manga.title) or 'No title')}/{chapter.chapter}/"
    click.echo(f"Downloading to {path}")
    os.makedirs(path, exist_ok=True)
    md.download(chapter, path)


def main():
    try:
        cli()
    except MdException as e:
        debug(e.args[0])
