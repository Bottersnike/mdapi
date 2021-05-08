from ..util import PaginatedRequest, _type_id
from ..endpoints import Endpoints
from ..schema import Type, ReadingStatus
from ..schema_new import NewManga, EditManga


class MangaAPI:
    def __init__(self, api):
        self.api = api

    def search(
        self,
        limit=10, offset=0, title=None, authors=None, artists=None,
        year=None, includedTags=None, includedTagsMode=None, excludedTags=None,
        excludedTagsMode=None, status=None, originalLanguage=None,
        publicationDemographic=None, ids=None, contentRating=None,
        createdAt=None
    ):
        return PaginatedRequest(self.api, Endpoints.Manga.SEARCH, params={
            "limit": limit, "offset": offset, "title": title,
            "authors": authors, "artists": artists, "year": year,
            "includedTags[]": includedTags, "includedTagsMode": includedTagsMode,
            "excludedTags[]": excludedTags, "excludedTagsMode": excludedTagsMode,
            "status": status, "originalLanguage": originalLanguage,
            "publicationDemographic": publicationDemographic, "ids": ids,
            "contentRating": contentRating, "createdAt": createdAt
        })

    def get(self, manga):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Manga.GET,
            urlparams={"manga": _type_id(manga)}
        ))

    def delete(self, manga):
        self.api._make_request(
            Endpoints.Manga.DELETE,
            urlparams={"manga": _type_id(manga)}
        )

    def follow(self, manga):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Manga.FOLLOW,
            urlparams={"manga": _type_id(manga)}
        ))

    def unfollow(self, manga):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Manga.UNFOLLOW,
            urlparams={"manga": _type_id(manga)}
        ))

    def get_tags(self):
        return [
            Type.parse_obj(i.get("data"))
            for i in self.api._make_request(Endpoints.Manga.TAGS)
        ]

    def get_random(self):
        return Type.parse_obj(self.api._make_request(Endpoints.Manga.RANDOM))

    def create(self, manga: NewManga):
        return self.api._make_request(Endpoints.Manga.CREATE, manga.dict())

    def edit(self, manga: EditManga):
        data = manga.dict()
        data.pop("id", None)
        return self.api._make_request(
            Endpoints.Manga.EDIT, data,
            urlparams={"manga": _type_id(manga)}
        )

    def get_chapters(self, manga, locales=None):
        return PaginatedRequest(
            self.api,
            Endpoints.Manga.CHAPTERS,
            urlparams={"manga": _type_id(manga)},
            params={"locales[]": locales}
        )

    def get_read(self, manga):
        return self.api._make_request(
            Endpoints.Manga.MARK_READ,
            urlparams={"manga": _type_id(manga)}
        )

    def set_status(self, manga, status: ReadingStatus):
        return self.api._make_request(
            Endpoints.Manga.SET_STATUS,
            urlparams={"manga": _type_id(manga)},
            body={"status": status}
        )

    def add_to_list(self, manga, list):
        self.api._make_request(
            Endpoints.Manga.ADD_TO_LIST,
            urlparams={"manga": _type_id(manga), "list": _type_id(list)}
        )

    def remove_from_list(self, manga, list):
        self.api._make_request(
            Endpoints.Manga.REMOVE_FROM_LIST,
            urlparams={"manga": _type_id(manga), "list": _type_id(list)}
        )
