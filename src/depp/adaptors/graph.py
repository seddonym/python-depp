from typing import List, Optional

from ..domain.valueobjects import DirectImport, Module, ImportPath
from depp.application.ports import graph


class NetworkXBackedImportGraph(graph.AbstractImportGraph):
    def add_import(self, direct_import: DirectImport) -> None:
        ...

    def remove_import(self, direct_import: DirectImport) -> None:
        ...

    def find_downstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> List[Module]:
        ...

    def find_upstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> List[Module]:
        ...

    def find_shortest_path(
        self, downstream_module: Module, upstream_module: Module
    ) -> Optional[ImportPath]:
        ...

