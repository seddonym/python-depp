from typing import Union

from depp.domain.valueobjects import ValueObject


class File(ValueObject):
    def __init__(self, name: str) -> None:
        self.name

    def __str__(self) -> str:
        return self.name


class Directory(ValueObject):
    def __init__(self, name: str, contents: List[Union[File, Directory]]) -> None:
        self.name

    def __str__(self) -> str:
        return self.name
