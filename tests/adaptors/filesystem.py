from typing import List, Tuple, Any, Dict

import yaml

from depp.application.ports.filesystem import AbstractFileSystem


class FakeFileSystem(AbstractFileSystem):
    def __init__(self, contents: str = None) -> None:
        """
        Args:
            contents: a string in the following format:

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
        self.contents = self._parse_contents(contents)

    def dirname(self, filename: str) -> str:
        """
        Return the full path to the directory name of the supplied filename.

        E.g. '/path/to/filename.py' will return '/path/to'.
        """
        return self.split(filename)[0]

    def walk(self, directory_name):
        """
        Given a directory, walk the file system recursively.

        For each directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        try:
            directory_contents = self.contents[directory_name]
        except KeyError:
            return []

        return self._walk_contents(directory_contents, containing_directory=directory_name)

    def _walk_contents(
        self, directory_contents: Dict[str, Any], containing_directory: str
    ) -> Tuple[str, List[str], List[str]]:
        tuples = []

        directories = []
        files = []
        for key, value in directory_contents.items():
            if value is None:
                files.append(key)
            else:
                directories.append(key)

        tuples.append(
            (containing_directory, directories, files)
        )

        if directories:
            for directory in directories:
                child_tuples = self._walk_contents(
                    directory_contents=directory_contents[directory],
                    containing_directory=self.join(containing_directory, directory),
                )
                if child_tuples:
                    tuples.extend(child_tuples)

        return tuples

    def join(self, *components: List[str]) -> str:
        return '/'.join(components)

    def split(self, file_name: str) -> List[str]:
        components = file_name.split('/')
        return ('/'.join(components[:-1]), components[-1])

    def _parse_contents(self, raw_contents: str):
        """
        Returns the raw contents parsed in the form:
            {
                '/path/to/mypackage': {
                    '__init__.py': None,
                    'foo': {
                        '__init__.py': None,
                        'one.py': None,
                        'two': {
                            '__init__.py': None,
                            'blue.py': None,
                            'green.py': None,
                        }
                    }
                }
            }
        """
        if raw_contents is None:
            return {}

        # Convert to yaml for ease of parsing.
        yamlified_lines = []
        raw_lines = [line for line in raw_contents.split('\n') if line.strip()]

        # Dedent all lines by the same amount.
        first_line = raw_lines[0]
        first_line_indent = len(first_line) - len(first_line.lstrip())
        dedented = lambda line: line[first_line_indent:]
        dedented_lines = map(dedented, raw_lines)

        for line in dedented_lines:
            trimmed_line = line.rstrip().rstrip('/')
            yamlified_line = trimmed_line + ':'
            yamlified_lines.append(yamlified_line)

        yamlified_string = '\n'.join(yamlified_lines)
        
        return yaml.load(yamlified_string)
