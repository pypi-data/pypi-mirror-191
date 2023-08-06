from dircleaner import cli
import click
from click.testing import CliRunner
import pytest
from pathlib import Path
import utils


def test_parse_json_mappings_valid_mappings(tmp_path: Path):
    json_file = tmp_path.joinpath("mapping.json")
    utils.create_json_file(json_file)
    dst_dir = tmp_path.joinpath("tmp-dir")
    dst_dir.mkdir()
    cli.load_dir_to_ext_dict(json_file, dst_dir)


def test_parse_json_mappings_invalid_json(tmp_path: Path):
    json_file = tmp_path.joinpath("mapping.json")
    dst_dir = tmp_path.joinpath("tmp-dir")
    utils.create_invalid_json_file(json_file)

    with pytest.raises(click.ClickException):
        cli.load_dir_to_ext_dict(json_file, dst_dir)


# test CLI


def test_success_valid_dir(tmp_path: Path):
    runner = CliRunner()
    with runner.isolated_filesystem(tmp_path):
        dir_name = "directory"
        dir_path = Path(dir_name)
        dir_path.mkdir()
        result = runner.invoke(cli.app, ["-f", dir_name])
    assert result.exit_code == 0


def test_fails_invalid_dir(tmp_path: Path):
    runner = CliRunner()
    with runner.isolated_filesystem(tmp_path):
        result = runner.invoke(cli.app, ["invalid-dir"])
    assert result.exit_code != 0


def test_success_valid_json_file(tmp_path: Path):

    dir_name = "directory"
    directory = Path(dir_name)
    json_filename = "mapping.json"
    json_path = Path(json_filename)
    # run in an empty directory
    runner = CliRunner()
    with runner.isolated_filesystem(tmp_path):
        utils.create_json_file(json_path)
        directory.mkdir()
        result = runner.invoke(cli.app, ["--json-file", json_filename, dir_name])
    assert result.exit_code == 0


def test_fails_invalid_json_file(tmp_path: Path):

    dir_name = "directory"
    directory = Path(dir_name)
    json_filename = "mapping.json"
    json_path = Path(json_filename)
    # run in an empty directory
    runner = CliRunner()
    with runner.isolated_filesystem(tmp_path):
        utils.create_invalid_json_file(json_path)
        directory.mkdir()
        result = runner.invoke(cli.app, ["--json-file", json_filename, "-f", dir_name])
    assert result.exit_code != 0


def test_fails_directory_contains_a_file_with_name_of_subdirectory(tmp_path: Path):
    dir_name = "directory"
    directory = Path(dir_name)
    # run in an empty directory
    runner = CliRunner()
    with runner.isolated_filesystem(tmp_path):
        directory.mkdir()
        invalid_file = directory / "documents"
        invalid_file.touch()
        result = runner.invoke(cli.app, ["-f", dir_name])
    assert result.exit_code != 0
