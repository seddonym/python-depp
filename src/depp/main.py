from .application.config import settings
from .adaptors.importscanner import ImportScanner
from .adaptors.modulefinder import ModuleFinder
from .adaptors.graph import NetworkXBackedImportGraph


settings.configure(
    IMPORT_GRAPH_CLASS=NetworkXBackedImportGraph,
    MODULE_FINDER_CLASS=ModuleFinder,
    IMPORT_SCANNER_CLASS=ImportScanner,
)
