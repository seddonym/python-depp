from depp.application import usecases
from depp.adaptors.graph import NetworkXBackedImportGraph
from depp.domain.valueobjects import Module, ImportPath

from tests.adaptors.filesystem import FakeFileSystem
from tests.adaptors.importscanner import FakeImportScanner
from tests.config import override_settings


class TestBuildGraph:
    def test_happy_path(self):
        file_system = FakeFileSystem(
            contents="""
                /path/to/mypackage/
                    __init__.py
                    foo/
                        __init__.py
                        one.py
                        two/
                            __init__.py
                            green.py
                            blue.py        
            """
        )
        module_imports = {
            Module('mypackage'): set(),
            Module('mypackage.foo'): set(),
            Module('mypackage.foo.one'): {Module('mypackage.foo.two.green')},
            Module('mypackage.foo.two'): set(),
            Module('mypackage.foo.two.green'): {Module('mypackage.foo.two.blue')},
            Module('mypackage.foo.two.blue'): set(),
        }
        import_scanner = FakeImportScanner(module_imports)

        with override_settings(
            FILE_SYSTEM=file_system,
            IMPORT_SCANNER=import_scanner,
        ):
            graph = usecases.build_graph('mypackage')

        assert set(module_imports.keys()) == graph.modules
        for module, imported_modules in module_imports.items():
            assert graph.fetch_modules_imported_by(module) == set(imported_modules)
