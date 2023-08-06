from typing import TypeAlias
from typing import TypedDict


class YASpeller(TypedDict, total=False):
    dictionary: list[str]


class Item(TypedDict):
    word: str


class Items(TypedDict):
    resource: str
    data: list[Item]


Report: TypeAlias = list[tuple[bool, Items]]
