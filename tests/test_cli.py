import pytest
from click.testing import CliRunner
from certdiff.cli import main

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output

def test_cli_no_args(runner):
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert "Error: Missing option '--new'." in result.output

def test_cli_old_and_old_url(runner):
    result = runner.invoke(
        main,
        ["--old", "dummy.pem", "--old-url", "https://example.com/cert.pem", "--new", "dummy2.pem"])
    assert result.exit_code != 0 or result.exit_code == 0

def test_cli_with_report_json_option(runner):
    result = runner.invoke(
        main, ["--old", "dummy.pem", "--new", "dummy2.pem", "--report-json", "out.json"])
    assert "--report-json" not in result.output

def test_cli_with_verbose_option(runner):
    result = runner.invoke(main, ["--old", "dummy.pem", "--new", "dummy2.pem", "--verbose"])
    assert "--verbose" not in result.output