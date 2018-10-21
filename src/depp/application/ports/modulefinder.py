from typing import Iterable
import abc

from depp.domain.valueobjects import Module


class AbstractModuleFinder(abc.ABC):
    """
    Finds Python modules inside a package.
    """
    def __init__(self, package_name: str) -> None:
        self.package_name = package_name

    @abc.abstractmethod
    def find_modules(self) -> Iterable[Module]:
        ...
