import pytest

from depp.adaptors.graph import NetworkXBackedImportGraph
from depp.domain.valueobjects import Module, DirectImport, ImportPath


class TestGraph:
    def test_add_module(self):
        graph = NetworkXBackedImportGraph()
        module = Module('foo')

        graph.add_module(module)

        assert graph.modules == {module}

    @pytest.mark.parametrize('add_module', (True, False))
    def test_add_import(self, add_module):
        graph = NetworkXBackedImportGraph()
        a, b = Module('foo'), Module('bar')

        if add_module:
            graph.add_module(a)

        graph.add_import(DirectImport(importer=a, imported=b))

        assert {a, b} == graph.modules
        assert {b} == graph.fetch_modules_imported_by(a)
        assert set() == graph.fetch_modules_imported_by(b)

    def test_remove_import(self):
        graph = NetworkXBackedImportGraph()
        a, b, c = Module('foo'), Module('bar'), Module('baz')
        graph.add_import(DirectImport(importer=a, imported=b))
        graph.add_import(DirectImport(importer=a, imported=c))

        graph.remove_import(DirectImport(importer=a, imported=b))

        assert {a, b, c} == graph.modules
        assert {c} == graph.fetch_modules_imported_by(a)

    def test_find_shortest_path(self):
        graph = NetworkXBackedImportGraph()
        a, b, c = Module('foo'), Module('bar'), Module('baz')
        graph.add_import(DirectImport(importer=a, imported=b))
        graph.add_import(DirectImport(importer=b, imported=c))

        assert ImportPath(a, b, c) == graph.find_shortest_path(
            upstream_module=a,
            downstream_module=c,
        )
