from typer.testing import CliRunner

from what_to_eat.main import app

runner = CliRunner()


def test_ls_without_config() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.output == "1.0.3\n"
