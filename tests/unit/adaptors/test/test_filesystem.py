from tests.adaptors.filesystem import FakeFileSystem


class TestFakeFileSystem:
    def test_directory_exists(self):
        file_system = FakeFileSystem("""
            /path/to/mypackage/
                __init__.py
                foo/
                    __init__.py
                    one.py
                    two/
                        __init__.py
                        green.py
                        blue.py
            /anotherpackage/
                another.txt                        
        """)
        assert [
            ('/path/to/mypackage', ['foo'], ['__init__.py']),
            ('/path/to/mypackage/foo', ['two'], ['__init__.py', 'one.py']),
            ('/path/to/mypackage/foo/two', [], ['__init__.py', 'green.py', 'blue.py']),
        ] == file_system.walk('/path/to/mypackage')

    def test_empty_if_directory_does_not_exist(self):
        file_system = FakeFileSystem("""
            /path/to/mypackage/
                __init__.py
        """)
        assert [] == file_system.walk('/path/to/nonexistent/package')

    def test_dirname(self):
        file_system = FakeFileSystem()
        assert '/path/to' == file_system.dirname('/path/to/file.txt')

    def test_join(self):
        file_system = FakeFileSystem()
        assert '/path/to/mypackage/file.py' == file_system.join('/path/to', 'mypackage', 'file.py')

    def test_split(self):
        file_system = FakeFileSystem()
        assert ('/path/to/mypackage', 'file.py') == file_system.split(
            '/path/to/mypackage/file.py')
