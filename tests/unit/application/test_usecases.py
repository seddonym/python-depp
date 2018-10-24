from depp.application import usecases
from depp.application.ports.graph import AbstractImportGraph


class TestBuildGraph:
    def test_happy_path(self):
        result = usecases.build_graph('mypackage')

        assert isinstance(result, AbstractImportGraph)
