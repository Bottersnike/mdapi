from devtools import debug
import click

from .mdapi import MdAPI, MdException
from .schema_new import NewManga
from .schema import LocalizedString


def _demo_follows(md: MdAPI):
    md.auth.login("user", "password")
    manga = md.manga.get("8dfbe01d-0dd5-4a3a-ba15-c773e6430053")
    # manga = md.manga.get("9929b4ed-58fb-40d0-8f5b-8d50747a85ef")
    debug(manga.title)
    md.manga.follow(manga)

    debug(list(md.user.get_followed_manga()))

    return

    ch = next(md.user.get_followed_chapters())
    debug(ch.id, ch.title)
    follow_manga = md.manga.get(md.chapter.get(ch).relationships[0].id)
    debug(follow_manga.id, follow_manga.title)
    md.manga.unfollow(follow_manga)

    ch = next(md.user.get_followed_chapters())
    debug(ch.id, ch.title)


def _demo_nologout(md):
    md.auth.login("BoTTersnIke", "password")
    debug(md.user.get_self().username)
    md.auth.logout()
    debug(md.user.get_self().username)
    md.auth.logout()
    debug(md.user.get_self().username)
    md.auth.refresh()


def _demo_author_search(md):
    results = md.author.search()
    for _ in range(5):
        debug(next(results))


def main():
    md = MdAPI()
    try:
        _demo_author_search(md)
    except MdException as e:
        click.echo(click.style("Request failed", fg="red"))
        debug(e.args[0])

    return

    # manga = md.manga.get("8dfbe01d-0dd5-4a3a-ba15-c773e6430053")
    # debug(manga.title)
    # list_ = md.list.get("cb224395-e510-4f2c-8416-6bfe88ac9708")
    list_ = md.list.create("name", "private", [])
    debug(list_)
    md.list.delete(list_)
    md.list.delete(list_)

    # md.manga.remove_from_list(manga, list_)

    feed = md.list.get_feed(list_)
    debug(next(feed))


    return

    md.auth.login("user", "password")
    debug(md.user.get_self().id)
    md.auth.refresh()
    md.auth.refresh()
    md.auth.logout()
    md.auth.refresh()

    return

    md.auth.logout()
    try:
        debug(md.user.get_self())
    except MdException as e:
        click.echo(click.style("Request failed", fg="red"))
        debug(e.args[0])
    return

    create = md.account.create("demo2", "password", "a2@b.com")
    debug(create)
    md.auth.login("demo2", "password")
    debug(md.api._auth)

    return

    # debug(md.account.create("uname", "password", "a@b.com"))
    debug(md.auth.login("user", "password"))
    self = md.user.get_self()
    debug(self)

    # debug(list(md.user.get_list()))
    # debug(list(md.user.get_list_for("573afd4a-203e-4fe0-909f-c94dfa877418")))

    group = md.group.get("70533611-26b6-4fe7-b77a-cf93f559e253")
    debug(group)
    debug(md.group.edit(group, leader="573afd4a-203e-4fe0-909f-c94dfa877418"))
    # debug(md.group.edit("70533611-26b6-4fe7-b77a-cf93f559e253", members=[
    #     # "573afd4a-203e-4fe0-909f-c94dfa877418",
    #     self.id
    # ]))
    # debug(md.group.create("test group", self.id, []))

    return


    md.login("user", "password")


    # debug(md.get_user())
    # for n, i in enumerate(md.get_manga_tags()):
    #     debug(n, i)
    #     if n == 10:
    #         break
    # return
    # print(md._auth)
    # debug(md.check_auth())
    # return

    manga = NewManga(
        title=LocalizedString("Test title"),
        altTitles=[],
        description=LocalizedString("Test description"),
        authors=[],
        artists=[],
        originalLanguage="en",
        # lastVolume=1,
        # lastChapter=1,
        publicationDemographic="josei",
        status="ongoing",
        year=2077,
        contentRating="safe",
        modNotes="Can I set these?",
    )
    manga = md.get_random_manga()
    debug(manga)
    # print(manga.dict())
    # changes = EditManga.parse_obj(manga.dict())
    # changes.modNotes = "The quick brown fox"
    # # print(chapgei)
    # debug(md.edit_manga(changes))
    # return
    print(manga.json())
    # print(md.create_manga(manga))

    # print("Manga: " + manga.title.text)
    # chapters = md.get_chapters(manga)
    # for i in chapters:
    #     debug(md.get_md_at_home_url(i))
    #     # debug(i)
    #     break

    # for i in md.search_manga():
    #     print(i.id)
    #     break
    # print(md.check_auth())
