import pytest


from depp.application.config import settings
from depp.adaptors.graph import NetworkXBackedImportGraph
from depp.adaptors.modulefinder import ModuleFinder

from tests.adaptors.importscanner import FakeImportScanner


@pytest.fixture(scope='module', autouse=True)
def configure_unit_tests():
    settings.configure(
        IMPORT_GRAPH_CLASS=NetworkXBackedImportGraph,
        MODULE_FINDER=ModuleFinder(),
        IMPORT_SCANNER=FakeImportScanner(),
        FILE_SYSTEM=None,
    )
