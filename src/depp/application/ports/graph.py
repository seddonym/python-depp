import abc
from typing import List, Optional

from depp.domain.valueobjects import DirectImport, Module, ImportPath


class AbstractImportGraph(abc.ABC):
    @abc.abstractmethod
    def add_import(self, direct_import: DirectImport) -> None:
        ...

    @abc.abstractmethod
    def remove_import(self, direct_import: DirectImport) -> None:
        ...

    @abc.abstractmethod
    def find_downstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> List[Module]:
        """
        Return a list of all the modules that import (even directly) the supplied module.
        Args:
            module: The upstream Module.
            search_descendants: Whether to find modules downstream of the *descendants* of the
                                upstream Module too.

        Usage:
            # Returns the modules downstream of mypackage.foo.
            import_graph.find_downstream_modules(
                Module('mypackage.foo'),
            )
            # Returns the modules downstream of mypackage.foo, mypackage.foo.one and
            mypackage.foo.two.
            import_graph.find_downstream_modules(
                Module('mypackage.foo'),
                search_descendants=True,
            )
        """
        ...

    @abc.abstractmethod
    def find_upstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> List[Module]:
        """
        Return a list of all the modules that are imported (even directly) by the supplied module.

        Args:
            module: The downstream Module.
            search_descendants: Whether to find modules upstream of the *descendants* of the
                                downstream Module too.
        """
        ...

    @abc.abstractmethod
    def find_shortest_path(
        self, downstream_module: Module, upstream_module: Module
    ) -> Optional[ImportPath]:
        ...