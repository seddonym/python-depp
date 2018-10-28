from typing import List
import os

from depp.application.ports.filesystem import AbstractFileSystem


class FakeFileSystem(AbstractFileSystem):
    def __init__(self, contents: str) -> None:
        self.contents = self._parse_contents(contents)

    def dirname(self, filename: str) -> str:
        """
        Return the full path to the directory name of the supplied filename.

        E.g. '/path/to/filename.py' will return '/path/to'.
        """
        ...

    def walk(self, directory_name):
        """
        Given a directory, walk the file system recursively.

        For each directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        """
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
        return (
            ('/path/to/mypackage', ['foo'], ['__init__.py']),
            ('/path/to/mypackage/foo', ['two'], ['__init__.py', 'one.py']),
            ('/path/to/mypackage/foo/two', [], ['__init__.py', 'green.py', 'blue.py']),
        )

    def join(self, *components: List[str]) -> str:
        return os.path.join(*components)

    def split(self, file_name: str) -> List[str]:
        return os.path.split(file_name)

    def _parse_contents(self, raw_contents: str):
        return []
