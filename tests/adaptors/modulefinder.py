from typing import Iterable, List

from depp.application.ports.modulefinder import AbstractModuleFinder
from depp.domain.valueobjects import Module





class StubModuleFinder(AbstractModuleFinder):
    """
    ModuleFinder for tests.
    """
    def __init__(self, *args, file_structure, **kwargs):
        self.file_structure = file_structure
        super().__init__(*args, **kwargs)

    def find_modules(self) -> Iterable[Module]:
        return []
