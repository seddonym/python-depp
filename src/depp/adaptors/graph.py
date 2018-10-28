from typing import Set, Optional

import networkx  # type: ignore
from networkx.algorithms import shortest_path  # type: ignore

from depp.application.ports import graph
from depp.domain.valueobjects import DirectImport, Module, ImportPath


class NetworkXBackedImportGraph(graph.AbstractImportGraph):
    def __init__(self) -> None:
        self._networkx_graph = networkx.DiGraph()

    @property
    def modules(self) -> Set[Module]:
        all_modules = set()
        for module_name in self._networkx_graph.nodes:
            all_modules.add(Module(module_name))
        return all_modules

    def add_module(self, module: Module) -> None:
        self._networkx_graph.add_node(module.name)

    def add_import(self, direct_import: DirectImport) -> None:
        self._networkx_graph.add_edge(direct_import.importer.name, direct_import.imported.name)

    def remove_import(self, direct_import: DirectImport) -> None:
        self._networkx_graph.remove_edge(direct_import.importer.name, direct_import.imported.name)

    def find_downstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> Set[Module]:
        raise NotImplementedError

    def find_upstream_modules(
        self, module: Module, search_descendants: bool = False
    ) -> Set[Module]:
        raise NotImplementedError

    def find_shortest_path(
        self, downstream_module: Module, upstream_module: Module
    ) -> Optional[ImportPath]:
        try:
            path = shortest_path(self._networkx_graph,
                                 downstream_module.name,
                                 upstream_module.name)
        except networkx.NetworkXNoPath:
            return None

        path = tuple(path)

        return path

    def fetch_modules_imported_by(self, module: Module) -> Set[Module]:
        imported_modules = set()
        for imported_module_name in self._networkx_graph.successors(module.name):
            imported_modules.add(
                Module(imported_module_name)
            )
        return imported_modules
