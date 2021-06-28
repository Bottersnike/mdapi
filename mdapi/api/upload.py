from typing import List, BinaryIO
from pydantic.decorator import validate_arguments

from ..endpoints import Endpoints
from ..schema import (
    TypeOrId, Type, Manga, ScanlationGroup, UploadSession, UploadSessionFile
)
from ..util import _type_id
from .base import APIBase


class UploadAPI(APIBase):
    def get_session(self):
        return Type.parse_obj(
            self.api._make_request(Endpoints.Upload.GET_SESSION)
        )

    @validate_arguments
    def begin(
        self,
        manga: TypeOrId[Manga],
        groups: List[TypeOrId[ScanlationGroup]]
    ):
        return Type.parse_obj(
            self.api._make_request(Endpoints.Upload.BEGIN, body={
                "manga": manga, "groups": groups
            })
        )

    def upload_images(
        self,
        session: TypeOrId[UploadSession],
        files: List[BinaryIO]
    ):
        files = {f"file{n + 1}": i for n, i in enumerate(files)}
        return [
            Type.parse_obj(i.get("data"))
            for i in self.api._make_request(
                Endpoints.Upload.ADD_IMAGE.format(session=_type_id(session)),
                files=files
            )
        ]

    @validate_arguments
    def delete_image(
        self,
        session: TypeOrId[UploadSession],
        file: TypeOrId[UploadSessionFile]
    ):
        self.api._make_request(
            Endpoints.Upload.DELETE_IMAGE.format(session=session, file=file)
        )

    @validate_arguments
    def abandon(self, session: TypeOrId[UploadSession]):
        self.api._make_request(Endpoints.Upload.ABADON.format(session=session))

    @validate_arguments
    def commit(
        self,
        session: TypeOrId[UploadSession],
        page_order: TypeOrId[UploadSessionFile],
        volume: str,
        chapter: str,
        title: str,
        translated_language: str
    ):
        return Type.parse_obj(self.api._make_request(
            Endpoints.Upload.COMMIT.format(session=session),
            body={
                "chapterDraft": {
                    "volume": volume,
                    "chapter": chapter,
                    "title": title,
                    "translatedLanguage": translated_language,
                },
                "pageOrder": page_order
            }
        ))
