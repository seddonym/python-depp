import pytest


from depp.application.config import settings
from depp.adaptors.graph import NetworkXBackedImportGraph

from tests.adaptors.importscanner import ImportScanner
from tests.adaptors.modulefinder import ModuleFinder


@pytest.fixture(scope='module', autouse=True)
def configure_unit_tests():
    settings.configure(
        IMPORT_GRAPH_CLASS=NetworkXBackedImportGraph,
        MODULE_FINDER_CLASS=ModuleFinder,
        IMPORT_SCANNER_CLASS=ImportScanner,
    )
