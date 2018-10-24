import pytest
from click.testing import CliRunner

# from depp.cli import main


@pytest.mark.skip
def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == '()\n'
    assert result.exit_code == 0
