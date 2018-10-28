from typing import Iterable, Dict

from depp.application.ports.importscanner import AbstractImportScanner
from depp.domain.valueobjects import DirectImport, SafeFilenameModule, Module


class FakeImportScanner(AbstractImportScanner):
    def __init__(self, import_map: Dict[Module, Iterable[Module]] = None) -> None:
        """
        Args:
            import_map: map of the imports within each module. Keys are each module,
                        values are lists of modules that the module directly imports.

        Example:

            To emulate a module foo.one that imports foo.two and foo.three, do:

                import_scanner = FakeImportScanner({
                    Module('foo.one'): (Module('foo.two'), Module('foo.three')),
                })

        """
        self.import_map = import_map if import_map else {}

    def scan_for_imports(self, module: SafeFilenameModule) -> Iterable[DirectImport]:
        module = module.as_module()
        try:
            imported_modules = self.import_map[module]
        except KeyError:
            return []

        build_direct_import = lambda imported_module: DirectImport(
            importer=module,
            imported=imported_module
        )

        return map(build_direct_import, imported_modules)
