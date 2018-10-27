from typing import List

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
        ...

    def join(self, *components: List[str]) -> str:
        ...

    def split(self, file_name: str) -> List[str]:
        ...

    def _parse_contents(self, raw_contents: str):
        return []
