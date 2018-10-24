from typing import Iterable

from depp.application.ports.importscanner import AbstractImportScanner
from depp.domain.valueobjects import DirectImport


class ImportScanner(AbstractImportScanner):
    def scan_for_imports(self) -> Iterable[DirectImport]:
        return []
