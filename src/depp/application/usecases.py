"""
Use cases handle application logic.
"""
from typing import List

from depp.application.ports.graph import AbstractImportGraph
from ..domain.valueobjects import Module
from .config import settings
from depp.application.ports.modulefinder import AbstractModuleFinder
from depp.application.ports.importscanner import AbstractImportScanner


def build_graph(package_name) -> AbstractImportGraph:
    """
    Build and return an import graph for the supplied package name.

    :return:
    """
    graph: AbstractImportGraph = settings.IMPORT_GRAPH_CLASS()

    # Build a list of all the Python modules in the package.
    module_finder: AbstractModuleFinder = settings.MODULE_FINDER_CLASS(package_name)
    modules = module_finder.find_modules()

    # Scan each module for imports and add them to the graph.
    import_scanner: AbstractImportScanner = settings.IMPORT_SCANNER_CLASS(modules)
    for direct_import in import_scanner.scan_for_imports():
        graph.add_import(direct_import)

    return graph


def report_upstream_modules(module_name: str) -> List[Module]:
    """
    Report on all the modules imported (directly or indirectly) by the supplied module and
    its descendants.
    """
    module = Module(module_name)
    graph = build_graph(module.package_name)
    modules = graph.find_upstream_modules(module, search_descendants=True)
    reporter = settings.UPSTREAM_MODULE_REPORTER()
    reporter.report(module, modules)


def report_downstream_modules(module_name: str) -> List[Module]:
    """
    Report on all the modules that import (directly or indirectly) the supplied module and
    its descendants.
    """
    module = Module(module_name)
    graph = build_graph(module.package_name)
    modules = graph.find_downstream_modules(module, search_descendants=True)
    reporter = settings.DOWNSTREAM_MODULE_REPORTER()
    reporter.report(module, modules)
