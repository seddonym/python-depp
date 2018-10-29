from depp.domain.valueobjects import SafeFilenameModule, Module, DirectImport

from tests.adaptors.importscanner import FakeImportScanner


def test_returns_imports():
    a = Module('foo')
    b = Module('bar')
    c = Module('baz')

    scanner = FakeImportScanner({
       a: {b, c},
    })

    result = scanner.scan_for_imports(SafeFilenameModule('foo', filename='something'))
    assert set(result) == {
        DirectImport(importer=a, imported=b),
        DirectImport(importer=a, imported=c),
    }


def test_when_no_imports_returns_empty_set():
    a = Module('foo')
    b = Module('bar')
    c = Module('baz')

    scanner = FakeImportScanner({
        a: {b, c},
    })

    result = scanner.scan_for_imports(SafeFilenameModule('bar', filename='something'))
    assert set(result) == set()
