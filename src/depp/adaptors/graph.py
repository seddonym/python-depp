from typing import Set, Optional

import networkx  # type: ignore
from networkx.algorithms import shortest_path, has_path  # type: ignore

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

    def find_modules_directly_imported_by(self, module: Module) -> Set[Module]:
        imported_modules = set()
        for imported_module_name in self._networkx_graph.successors(module.name):
            imported_modules.add(
                Module(imported_module_name)
            )
        return imported_modules

    def find_modules_that_directly_import(self, module: Module) -> Set[Module]:
        importers = set()
        for importer_name in self._networkx_graph.predecessors(module.name):
            importers.add(
                Module(importer_name)
            )
        return importers

    def find_downstream_modules(
        self, module: Module, as_subpackage: bool = False
    ) -> Set[Module]:
        # TODO optimise for as_subpackage.
        source_modules = {module}
        if as_subpackage:
            source_modules.update(self.find_descendants(module))

        downstream_modules = set()

        for candidate in filter(lambda m: m not in source_modules, self.modules):
            for source_module in source_modules:
                if has_path(self._networkx_graph, source_module.name, candidate.name):
                    downstream_modules.add(candidate)
                    break

        return downstream_modules

    def find_upstream_modules(
        self, module: Module, as_subpackage: bool = False
    ) -> Set[Module]:
        upstream_modules = set()
        if as_subpackage:
            raise NotImplementedError
        modules_other_than_this_one = lambda m: m != module
        for candidate in filter(modules_other_than_this_one, self.modules):
            if has_path(self._networkx_graph, candidate.name, module.name):
                upstream_modules.add(candidate)
        return upstream_modules

    def find_children(self, module: Module) -> Set[Module]:
        children = set()
        for potential_child in self.modules:
            if potential_child.is_child_of(module):
                children.add(potential_child)
        return children

    def find_descendants(self, module: Module) -> Set[Module]:
        descendants = set()
        for potential_descendant in self.modules:
            if potential_descendant.is_descendant_of(module):
                descendants.add(potential_descendant)
        return descendants

    def find_shortest_path(
        self, upstream_module: Module, downstream_module: Module,
    ) -> Optional[ImportPath]:
        try:
            path = shortest_path(self._networkx_graph,
                                 source=upstream_module.name,
                                 target=downstream_module.name)
        except networkx.NetworkXNoPath:
            return None

        return ImportPath(*map(Module, path))

    def find_shortest_paths(
        self, upstream_modules: Set[Module], downstream_modules: Set[Module],
    ) -> Set[ImportPath]:
        raise NotImplementedError

    def add_module(self, module: Module) -> None:
        self._networkx_graph.add_node(module.name)

    def add_import(self, direct_import: DirectImport) -> None:
        self._networkx_graph.add_edge(direct_import.importer.name, direct_import.imported.name)

    def remove_import(self, direct_import: DirectImport) -> None:
        self._networkx_graph.remove_edge(direct_import.importer.name, direct_import.imported.name)

