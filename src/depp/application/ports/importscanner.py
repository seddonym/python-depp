import abc
from typing import Iterable

from depp.domain.valueobjects import Module, DirectImport


class AbstractImportScanner(abc.ABC):
    """
    Statically analyses some Python modules for import statements within their shared package.
    """
    @abc.abstractmethod
    def scan_for_imports(self, modules: Iterable[Module]) -> Iterable[DirectImport]:
        ...
