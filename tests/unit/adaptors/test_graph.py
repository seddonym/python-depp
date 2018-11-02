import pytest

from depp.adaptors.graph import NetworkXBackedImportGraph
from depp.domain.valueobjects import Module, DirectImport, ImportPath


def test_modules_when_empty():
    graph = NetworkXBackedImportGraph()
    assert graph.modules == set()
    

def test_find_modules_directly_imported_by():
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo'), Module('bar'), Module('baz')
    d, e, f = Module('foo.one'), Module('bar.one'), Module('baz.one')

    graph.add_import(DirectImport(importer=a, imported=b))
    graph.add_import(DirectImport(importer=a, imported=c))
    graph.add_import(DirectImport(importer=a, imported=d))
    graph.add_import(DirectImport(importer=b, imported=e))
    graph.add_import(DirectImport(importer=f, imported=a))

    assert {b, c, d} == graph.find_modules_directly_imported_by(Module('foo'))


def test_find_modules_that_directly_import():
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo'), Module('bar'), Module('baz')
    d, e, f = Module('foo.one'), Module('bar.one'), Module('baz.one')

    graph.add_import(DirectImport(importer=a, imported=b))
    graph.add_import(DirectImport(importer=a, imported=c))
    graph.add_import(DirectImport(importer=a, imported=d))
    graph.add_import(DirectImport(importer=b, imported=e))
    graph.add_import(DirectImport(importer=f, imported=b))

    assert {a, f} == graph.find_modules_that_directly_import(Module('bar'))


class TestFindDownstreamModules:
    @pytest.mark.parametrize(
        'module, expected_result', (
            (Module('a'), {Module('b'), Module('c'), Module('d'), Module('e')}),
            (Module('e'), set()),
        )
    )
    def test_without_descendants(self, module, expected_result):
        graph = NetworkXBackedImportGraph()
        a, b, c = Module('a'), Module('b'), Module('c')
        d, e, f = Module('d'), Module('e'), Module('f')

        graph.add_import(DirectImport(importer=a, imported=b))
        graph.add_import(DirectImport(importer=a, imported=c))
        graph.add_import(DirectImport(importer=c, imported=d))
        graph.add_import(DirectImport(importer=d, imported=e))
        graph.add_import(DirectImport(importer=f, imported=b))

        assert expected_result == graph.find_downstream_modules(module)

    def test_with_descendants(self):
        assert False


class TestFindUpstreamModules:
    @pytest.mark.parametrize(
        'module, expected_result', (
            (Module('e'), {Module('d'), Module('c'), Module('a')}),
            (Module('a'), set()),
        )
    )
    def test_without_descendants(self, module, expected_result):
        graph = NetworkXBackedImportGraph()
        a, b, c = Module('a'), Module('b'), Module('c')
        d, e, f = Module('d'), Module('e'), Module('f')

        graph.add_import(DirectImport(importer=a, imported=b))
        graph.add_import(DirectImport(importer=a, imported=c))
        graph.add_import(DirectImport(importer=c, imported=d))
        graph.add_import(DirectImport(importer=d, imported=e))
        graph.add_import(DirectImport(importer=f, imported=b))

        assert expected_result == graph.find_upstream_modules(module)

    def test_with_descendants(self):
        assert False


@pytest.mark.parametrize(
    'module, expected_result', (
        (Module('foo'), {Module('foo.a'), Module('foo.b'), Module('foo.c')}),
        (Module('foo.a'), {Module('foo.a.one')}),
        (Module('foo.c'), set()),
    )
)
def test_find_children(module, expected_result):
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo.a'), Module('foo.b'), Module('foo.c')
    d, e, f = Module('foo.a.one'), Module('foo.b.one'), Module('bar.g')

    for module_to_add in (a, b, c, d, e, f):
        graph.add_module(module_to_add)

    assert expected_result == graph.find_children(module)


@pytest.mark.parametrize(
    'module, expected_result', (
        (Module('foo'), {Module('foo.a'), Module('foo.b'), Module('foo.c'),
                         Module('foo.a.one'), Module('foo.b.one')}),
        (Module('foo.a'), {Module('foo.a.one')}),
        (Module('foo.c'), set()),
    )
)
def test_find_descendants(module, expected_result):
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo.a'), Module('foo.b'), Module('foo.c')
    d, e, f = Module('foo.a.one'), Module('foo.b.one'), Module('bar.g')

    for module_to_add in (a, b, c, d, e, f):
        graph.add_module(module_to_add)

    assert expected_result == graph.find_descendants(module)


def test_find_shortest_path_when_exists():
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo'), Module('bar'), Module('baz')
    d, e, f = Module('long'), Module('way'), Module('around')

    # Add short path.
    graph.add_import(DirectImport(importer=a, imported=b))
    graph.add_import(DirectImport(importer=b, imported=c))

    # Add longer path.
    graph.add_import(DirectImport(importer=a, imported=d))
    graph.add_import(DirectImport(importer=d, imported=e))
    graph.add_import(DirectImport(importer=e, imported=f))
    graph.add_import(DirectImport(importer=f, imported=c))

    assert ImportPath(a, b, c) == graph.find_shortest_path(
        upstream_module=a,
        downstream_module=c,
    )

def test_find_shortest_path_returns_none_if_not_exists():
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo'), Module('bar'), Module('baz')

    graph.add_import(DirectImport(importer=a, imported=b))
    graph.add_import(DirectImport(importer=b, imported=c))

    assert None == graph.find_shortest_path(
        upstream_module=c,
        downstream_module=a,
    )

def test_find_shortest_paths():
    assert False


def test_add_module():
    graph = NetworkXBackedImportGraph()
    module = Module('foo')

    graph.add_module(module)

    assert graph.modules == {module}


@pytest.mark.parametrize('add_module', (True, False))
def test_add_import(add_module):
    graph = NetworkXBackedImportGraph()
    a, b = Module('foo'), Module('bar')

    # Adding the module should make no difference to the result.
    if add_module:
        graph.add_module(a)

    graph.add_import(DirectImport(importer=a, imported=b))

    assert {a, b} == graph.modules
    assert {b} == graph.find_modules_directly_imported_by(a)
    assert set() == graph.find_modules_directly_imported_by(b)


def test_remove_import():
    graph = NetworkXBackedImportGraph()
    a, b, c = Module('foo'), Module('bar'), Module('baz')
    graph.add_import(DirectImport(importer=a, imported=b))
    graph.add_import(DirectImport(importer=a, imported=c))

    graph.remove_import(DirectImport(importer=a, imported=b))

    assert {a, b, c} == graph.modules
    assert {c} == graph.find_modules_directly_imported_by(a)
