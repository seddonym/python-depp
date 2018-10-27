from depp.application import usecases
from depp.adaptors.graph import NetworkXBackedImportGraph

from tests.adaptors.filesystem import FakeFileSystem
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
        with override_settings(
            FILE_SYSTEM=file_system,
        ):
            result = usecases.build_graph('mypackage')

        assert isinstance(result, NetworkXBackedImportGraph)

        # TODO - what should we test here?
