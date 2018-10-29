from typing import Iterable, List

from ..domain.valueobjects import Module, SafeFilenameModule
from depp.application.ports import modulefinder
from depp.application.ports.filesystem import AbstractFileSystem


class ModuleFinder(modulefinder.AbstractModuleFinder):

    def find_modules(
        self, package_name: str, file_system: AbstractFileSystem
    ) -> Iterable[SafeFilenameModule]:
        self.file_system = file_system

        package_directory = self._determine_package_directory(package_name)

        modules: List[SafeFilenameModule] = []

        for module_filename in self._get_python_files_inside_package(package_directory):
            module_name = self._module_name_from_filename(module_filename, package_directory)
            modules.append(
                SafeFilenameModule(module_name, module_filename)
            )

        return modules

    def _get_python_files_inside_package(self, directory: str) -> Iterable[str]:
        """
        Get a list of Python files within the supplied package directory.
         Return:
            Generator of Python file names.
        """
        for dirpath, dirs, files in self.file_system.walk(directory):
            # Don't include directories that aren't Python packages,
            # nor their subdirectories.
            if '__init__.py' not in files:
                for d in list(dirs):
                    dirs.remove(d)
                continue

            # Don't include hidden directories.
            dirs_to_remove = [d for d in dirs if self._should_ignore_dir(d)]
            for d in dirs_to_remove:
                dirs.remove(d)

            for filename in files:
                if self._is_python_file(filename):
                    yield self.file_system.join(dirpath, filename)

    def _should_ignore_dir(self, directory: str) -> bool:
        # TODO: make this configurable.
        # Skip adding directories that are hidden, or look like Django migrations.
        return directory.startswith('.') or directory == 'migrations'

    def _is_python_file(self, filename: str) -> bool:
        """
        Given a filename, return whether it's a Python file.

        Args:
            filename (str): the filename, excluding the path.
        Returns:
            bool: whether it's a Python file.
        """
        return not filename.startswith('.') and filename.endswith('.py')

    def _module_name_from_filename(self, filename_and_path: str, package_directory: str) -> str:
        """
        Args:
            filename_and_path (string) - the full name of the Python file.
            package_directory (string) - the full path of the top level Python package directory.
         Returns:
            Absolute module name for importing (string).
        """
        container_directory, package_name = self.file_system.split(package_directory)
        internal_filename_and_path = filename_and_path[len(package_directory):]
        internal_filename_and_path_without_extension = internal_filename_and_path[1:-3]
        components = [package_name] + internal_filename_and_path_without_extension.split('/')
        if components[-1] == '__init__':
            components.pop()
        return '.'.join(components)

    def _determine_package_directory(self, package_name: str) -> str:
        return '/path/to/mypackage'
