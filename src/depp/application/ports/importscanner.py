import abc
from typing import Iterable

from depp.domain.valueobjects import Module, DirectImport


class AbstractImportScanner(abc.ABC):
    """
    Statically analyses some Python modules for import statements within their shared package.
    """
    def __init__(self, modules: Iterable[Module]) -> None:
        self.modules = modules

    @abc.abstractmethod
    def scan_for_imports(self) -> Iterable[DirectImport]:
        ...
