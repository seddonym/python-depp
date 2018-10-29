from typing import List
import abc


class AbstractFileSystem(abc.ABC):
    """
    Abstraction around file system calls.
    """
    @abc.abstractmethod
    def dirname(self, filename: str) -> str:
        """
        Return the full path to the directory name of the supplied filename.

        E.g. '/path/to/filename.py' will return '/path/to'.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def walk(self, directory_name):
        """
        Given a directory, walk the file system recursively.

        For each directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def join(self, *components: List[str]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def split(self, file_name: str) -> List[str]:
        raise NotImplementedError
