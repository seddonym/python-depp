from depp.application import usecases
from depp.adaptors.graph import NetworkXBackedImportGraph

from tests.adaptors.modulefinder import StubModuleFinder
from tests.valueobjects import File, Directory


class TestBuildGraph:
    def test_happy_path(self):
        # module_finder = StubModuleFinder(
        #     file_structure={
        #         File('__init__.py'),
        #         Directory(
        #             'foo',
        #             contents=[
        #                 File('.hidden'),
        #                 File('one.py'),
        #                 File('two.py'),
        #                 Directory('three',
        #                           contents=[
        #                               File()
        #                           ])
        #             ],
        #         ),
        #     },
        # )
        module_finder = StubModuleFinder(
            file_structure=(
                '__init__.py',
                (
                    'foo',
                    (
                        '__init__.py',
                        'one.py',
                        (
                            'two', (),
                        ),
                    ),
                ),
            ),
        )
        result = usecases.build_graph('mypackage', module_finder=module_finder)

        assert isinstance(result, NetworkXBackedImportGraph)

        # TODO - what should we test here?
