from typing import Iterable

from ..domain.valueobjects import Module
from depp.application.ports import modulefinder


class ModuleFinder(modulefinder.AbstractModuleFinder):
    def find_modules(self) -> Iterable[Module]:
        ...
