from depp.domain.valueobjects import Module, SafeFilenameModule, DirectImport, ImportPath


class TestModule:
    def test_repr(self):
        module = Module('foo.bar')
        assert repr(module) == '<Module: foo.bar>'

    def test_equals(self):
        a = Module('foo.bar')
        b = Module('foo.bar')
        c = Module('foo.bar.baz')

        assert a == b
        assert a != c
        # Also non-Module instances should not be treated as equal.
        assert a != 'foo'

    def test_hash(self):
        a = Module('foo.bar')
        b = Module('foo.bar')
        c = Module('foo.bar.baz')

        assert hash(a) == hash(b)
        assert hash(a) != hash(c)

    def test_package_name(self):
        assert Module('foo.bar.baz').package_name == 'foo'


class TestSafefilenameModule:
    def test_repr(self):
        module = SafeFilenameModule('foo.bar', filename='foo/bar.py')
        assert repr(module) == '<SafeFilenameModule: foo.bar (foo/bar.py)>'

    def test_equals(self):
        a = SafeFilenameModule('foo.bar', filename='foo/bar.py')
        b = SafeFilenameModule('foo.bar', filename='foo/bar.py')
        c = SafeFilenameModule('foo.bar.baz', filename='foo/bar.py')
        d = SafeFilenameModule('foo.bar', filename='different/bar.py')
        e = Module('foo.bar')

        assert a == b
        assert a != c
        assert a != d
        assert a != e

        # Also non-Module instances should not be treated as equal.
        assert a != 'foo'

    def test_hash(self):
        a = SafeFilenameModule('foo.bar', filename='foo/bar.py')
        b = SafeFilenameModule('foo.bar', filename='foo/bar.py')
        c = SafeFilenameModule('foo.bar.baz', filename='foo/bar.py')
        d = SafeFilenameModule('foo.bar', filename='different/bar.py')
        e = Module('foo.bar')

        assert hash(a) == hash(b)
        assert hash(a) != hash(c)
        assert hash(a) != hash(d)
        assert hash(a) != hash(e)

    def test_as_module(self):
        safe_filename_module = SafeFilenameModule('foo.bar', filename='foo/bar.py')

        result = safe_filename_module.as_module()

        assert result == Module('foo.bar')

class TestDirectImport:
    def test_repr(self):
        import_path = DirectImport(
            importer=Module('foo'), imported=Module('bar')
        )
        assert repr(import_path) == '<DirectImport: foo <- bar>'

    def test_equals(self):
        a = DirectImport(importer=Module('foo'), imported=Module('bar'))
        b = DirectImport(importer=Module('foo'), imported=Module('bar'))
        c = DirectImport(importer=Module('foo'), imported=Module('foo.baz'))

        assert a == b
        assert a != c
        # Also non-DirectImport instances should not be treated as equal.
        assert a != 'foo'


    def test_hash(self):
        a = DirectImport(importer=Module('foo'), imported=Module('bar'))
        b = DirectImport(importer=Module('foo'), imported=Module('bar'))
        c = DirectImport(importer=Module('bar'), imported=Module('foo'))

        assert hash(a) == hash(b)
        assert hash(a) != hash(c)


class TestImportPath:
    def test_repr(self):
        import_path = ImportPath(
            Module('one'),
            Module('two'),
            Module('three'),
        )
        assert repr(import_path) == '<ImportPath: three <- two <- one>'

    def test_equals(self):
        a = ImportPath(
            Module('one'),
            Module('two'),
            Module('three'),
        )
        b = ImportPath(
            Module('one'),
            Module('two'),
            Module('three'),
        )
        c = ImportPath(
            Module('one'),
            Module('three'),
            Module('two'),
        )

        assert a == b
        assert a != c
        # Also non-ImportPath instances should not be treated as equal.
        assert a != 'foo'

    def test_hash(self):
        a = ImportPath(
            Module('one'),
            Module('two'),
            Module('three'),
        )
        b = ImportPath(
            Module('one'),
            Module('two'),
            Module('three'),
        )
        c = ImportPath(
            Module('one'),
            Module('three'),
            Module('two'),
        )

        assert hash(a) == hash(b)
        assert hash(a) != hash(c)
