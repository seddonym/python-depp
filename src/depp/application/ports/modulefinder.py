from typing import Iterable
import abc

from depp.domain.valueobjects import Module

from .filesystem import AbstractFileSystem


class AbstractModuleFinder(abc.ABC):
    """
    Finds Python modules inside a package.
    """
    @abc.abstractmethod
    def find_modules(self, package_name: str, file_system: AbstractFileSystem) -> Iterable[Module]:
        """
        Searches the package for all importable Python modules.
        """
        ...
