from typing import List


class Module:
    ...


class DirectImport:
    """
    An import between one module and another.
    """
    def __init__(self, importer: Module, imported: Module) -> None:
        self.importer = importer
        self.imported = imported


class ImportPath:
    """
    A flow of imports between two modules, from upstream to downstream.
    """
    def __init__(self, *modules: List[Module]) -> Module:
        self.modules = modules
