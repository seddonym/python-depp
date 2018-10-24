from typing import Iterable, List

from depp.application.ports.modulefinder import AbstractModuleFinder
from depp.domain.valueobjects import Module


class ModuleFinder(AbstractModuleFinder):
    def find_modules(self) -> Iterable[Module]:
        return self._fake_modules

    def set_fake_modules(self, modules: List[str]) -> None:
        self._fake_modules = [Module[m] for m in modules]
