from depp.adaptors.modulefinder import ModuleFinder
from depp.domain.valueobjects import SafeFilenameModule


from tests.adaptors.filesystem import FakeFileSystem


def test_happy_path():
    module_finder = ModuleFinder()

    file_system = FakeFileSystem(contents="""
        /path/to/mypackage/
                    __init__.py
                    foo/
                        __init__.py
                        one.py
                        two/
                            __init__.py
                            green.py
                            blue.py   
        """)

    result = module_finder.find_modules(
        package_name='mypackage',
        file_system=file_system,
    )

    expected_modules = {
        SafeFilenameModule('mypackage',
                           filename='/path/to/mypackage/__init__.py'),
        SafeFilenameModule('mypackage.foo',
                           filename='/path/to/mypackage/foo/__init__.py'),
        SafeFilenameModule('mypackage.foo.one',
                           filename='/path/to/mypackage/foo/one.py'),
        SafeFilenameModule('mypackage.foo.two',
                           filename='/path/to/mypackage/foo/two/__init__.py'),
        SafeFilenameModule('mypackage.foo.two.green',
                           filename='/path/to/mypackage/foo/two/green.py'),
        SafeFilenameModule('mypackage.foo.two.blue',
                           filename='/path/to/mypackage/foo/two/blue.py'),
    }
    assert set(result) == expected_modules
