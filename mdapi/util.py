import base64
import json
import time
from typing import Generic, Iterable, List, TypeVar

from pydantic.main import BaseModel

from .schema import Type, TypeOrId


def _type_id(type: TypeOrId):
    if isinstance(type, Type):
        return type.id
    if isinstance(type, BaseModel):
        return type.id
    return type


def _get_token_expires(jwt):
    payload = jwt.split(".")[1]
    payload = json.loads(base64.b64decode(payload + "=="))
    return payload["exp"]


def _is_token_expired(jwt):
    return _get_token_expires(jwt) <= time.time()


T = TypeVar("T")


class PaginatedRequest(Generic[T]):
    _LIMIT = 100

    def __init__(self, api, *args, **kwargs):
        self.total = None
        self.offset = kwargs.pop("offset", 0)

        self._results = None
        self._limit = kwargs.pop("limit", self._LIMIT)
        self._params = kwargs.pop("params", {})
        self._api = api
        self._args = args
        self._kwargs = kwargs

        self._ensure_populated()

    def _get_next(self) -> None:
        results = self._api._make_request(*self._args, **self._kwargs, params={
            **self._params,
            "offset": self.offset,
            "limit": self._limit
        })
        self.total = results.get("total", 0)
        self.offset += results.get("limit", 0)
        self._results = results.get("results", [])

    def __iter__(self) -> Iterable[T]:
        return self

    def _ensure_populated(self) -> None:
        if self._results is None or len(self._results) == 0:
            if self.total is not None and self.offset >= self.total:
                raise StopIteration
            self._get_next()

    def __next__(self) -> T:
        self._ensure_populated()

        if len(self._results) == 0:
            raise StopIteration

        result = self._results.pop(0)
        result = result.get("data", result)
        return Type.parse_obj(result)

    def next_page(self) -> List[T]:
        try:
            self._ensure_populated()
        except StopIteration:
            return []
        res = self._results
        self._results = []
        res = [i.get("data", i) for i in res]
        return [Type.parse_obj(i) for i in res]


__all__ = (
    "_type_id", "_get_token_expires", "_is_token_expired", "PaginatedRequest"
)
