from types import FunctionType
from typing import Generator, List, Tuple
from pydantic import BaseModel

from .schema_enum import LanguageCode


class LocalizedString(dict):
    def __init__(self, text: str, lang: LanguageCode = "en"):
        self.lang = lang
        self.text = text

    def items(self) -> List[Tuple[LanguageCode, str]]:
        return [(self.lang, self.text)]

    def keys(self) -> List[LanguageCode]:
        return [self.lang]

    def values(self) -> List[str]:
        return [self.text]

    def __pretty__(self, fmt, **kwargs) -> Generator[str, None, None]:
        yield "<"
        yield self.lang
        yield " "
        yield fmt(self.text)
        yield ">"

    def __getitem__(self, key) -> str:
        if key != self.lang:
            raise ValueError
        return self.text

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.lang}:{self.text})"

    @classmethod
    def __get_validators__(cls) -> FunctionType:
        yield cls.return_i18n

    @classmethod
    def return_i18n(cls, values):
        return cls(*list(values.items())[0][::-1])


class Keyed:
    def __init__(self, item):
        self.item = item

    def __get_validators__(cls):
        yield cls.return_type

    def return_type(self, values):
        subclasses = self.item.__subclasses__()
        types = {
            i._type: i for i in subclasses
        }

        if "type" not in values:
            return None
        type = values["type"]

        if type not in types:
            raise KeyError(f"Incorrect type: {type}")
        return types[type](
            id=values["id"],
            relationships=values.get("relationships"),
            **values["attributes"]
        )


class KeyedUnion:
    def __class_getitem__(cls, item):
        class KeyedUnion(BaseModel):
            __root__: Keyed(item)

            def __new__(cls, *args, **kwargs):
                (self := object.__new__(cls)).__init__(*args, **kwargs)
                return self.__root__

            def __iter__(self):
                return iter(self.__root__)

            def __getitem__(self, item):
                return self.__root__[item]

            def __getattr__(self, item):
                return getattr(self.__root__, item)

            def dict(self):
                return self.__root__.dict()

        return KeyedUnion
