"""Tests to check that the project is properly baked."""
import importlib
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import pytest
from click.testing import CliRunner as ClickCliRunner
from cookiecutter.utils import rmtree
from typer.testing import CliRunner as TyperCliRunner

if sys.version_info < (3, 11):
    from tomli import load as toml_load
else:
    from tomllib import load as toml_load

INTERFACES = ["No command-line interface", "Click", "Typer", "Argparse"]


@contextmanager
def inside_dir(dirpath):
    """Execute code from inside the given directory.

    dirpath: str
        Path of the directory the command is being run.
    """
    old_path = Path.cwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """Delete the temporal directory that is created when executing the tests.

    cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the exit status.

    command:
        Command that will be executed
    dirpath:
        String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output."""
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    """Test the year in the license file."""
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.now(tz=timezone.utc).astimezone()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies."""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = Path(project_path) / "src" / project_slug
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    """Test the default structure and configuration of the baked project."""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        assert "src" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files

        assert result.project.join("src/python_boilerplate").isdir()


def test_bake_and_run_tests(cookies):
    """Test the baked project by running pytest inside its directory."""
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "y"}) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        assert run_inside_dir("poetry run pytest", str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break pyproject.toml."""
    with bake_in_temp_dir(cookies, extra_context={"full_name": 'name "quote" name'}) as result:
        assert result.project.isdir()
        assert run_inside_dir("poetry run pytest", str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break pyproject.toml."""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        assert run_inside_dir("poetry run pytest", str(result.project)) == 0


def test_bake_without_author_file(cookies):
    """Ensure that the authors files are removed."""
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.md" not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join("docs").listdir()]
        assert "authors.md" not in doc_files

        # Assert there are no spaces in the toc tree
        # docs_index_path = result.project.join("docs/index.md")
        # with Path.open(str(docs_index_path)) as index_file:
        #     assert "contributing\n   history" in index_file.read()


def test_bake_selecting_license(cookies):
    """Assert that the license is properly set."""
    license_strings = {
        "MIT": "MIT License",
        "BSD-3-Clause": "Redistributions of source code must retain the "
        "above copyright notice, this",
        "ISC": "ISC License",
        "Apache-2.0": "Licensed under the Apache License, Version 2.0",
        "GPL-3.0-only": "GNU GENERAL PUBLIC LICENSE",
    }
    for license_name, target_string in license_strings.items():
        context = {"open_source_license": license_name}
        with bake_in_temp_dir(cookies, extra_context=context) as result:
            # NOTE Path.open won't work properly for python<3.11
            with Path.open(result.project.join("LICENSE"), encoding="utf-8") as f:
                content = f.read()
                assert target_string in content
            with Path.open(result.project.join("pyproject.toml"), encoding="utf-8") as f:
                content = f.read()
                assert license_name in content
            # NOTE the lines below can induce encoding errors
            # assert target_string in result.project.join("LICENSE").read()
            # assert license_name in result.project.join("pyproject.toml").read()


def test_bake_not_open_source(cookies):
    """Ensure that license is removed for not open source projects."""
    with bake_in_temp_dir(
        cookies, extra_context={"open_source_license": "Not open source"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.md").read()


def test_not_using_pytest(cookies):
    """Ensure that pytest is not used when 'use_pytest' == 'n'."""
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "n"}) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import unittest" in "".join(lines)
        assert "import pytest" not in "".join(lines)


@pytest.mark.parametrize("interface", INTERFACES)
def test_bake_with_console_script_files(cookies, interface):
    """Ensure that the cli is properly set."""
    context = {"command_line_interface": interface}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)

    pyproject_path = Path(project_path) / "pyproject.toml"
    with Path.open(pyproject_path, encoding="utf-8") as pyproject_file:
        file_content = pyproject_file.read()

    if interface == "No command-line interface":
        assert "cli.py" not in found_project_files
        assert "[tool.poetry.scripts]" not in file_content
    else:
        assert "cli.py" in found_project_files
        assert "[tool.poetry.scripts]" in file_content


def test_bake_with_console_script_cli(cookies):
    """Test the baked project's command line interface using Click."""
    context = {"command_line_interface": "Click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = Path(project_dir) / "cli.py"
    module_name = f"{project_slug}.cli"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = ClickCliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = f"Replace this message by putting your code into {project_slug}.cli.main"
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_with_typer_console_script_cli(cookies):
    """Test the baked project's command line interface using Typer."""
    context = {"command_line_interface": "Typer"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = Path(project_dir) / "cli.py"
    module_name = f"{project_slug}.cli"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = TyperCliRunner()
    noarg_result = runner.invoke(cli.app)
    assert noarg_result.exit_code == 0
    noarg_output = f"Replace this message by putting your code into {project_slug}.cli.main"
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.app, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_with_argparse_console_script_cli(cookies, capsys):
    """Test the baked project's command line interface using argparse."""
    context = {"command_line_interface": "Argparse"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = project_dir / "cli.py"
    module_name = f"{project_slug}.cli"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)

    with mock.patch("argparse._sys.argv", ["cli"]):
        noarg_result = cli.main()
        assert noarg_result == 0
        out, err = capsys.readouterr()
        noarg_output = f"Replace this message by putting your code into {project_slug}"
        assert noarg_output in out

    # Mock the command line arguments for --help
    with mock.patch("argparse._sys.argv", ["cli", "--help"]):
        try:
            help_result = cli.main()
        except SystemExit as e:
            help_result = e.code

        assert help_result == 0

        out, err = capsys.readouterr()
        assert "show this help message" in out


@pytest.mark.parametrize(
    ("formatter", "expected"), [("Black", "black --check"), ("Ruff-format", "ruff"), ("No", None)]
)
def test_formatter(cookies, formatter, expected):
    """Ensure that the chosen formater is properly set."""
    formatter_to_dependency = {"Black": "black", "Ruff-format": "ruff", "No": None}

    with bake_in_temp_dir(cookies, extra_context={"formatter": formatter}) as result:
        assert result.project.isdir()
        pyproject_path = result.project.join("pyproject.toml")
        with Path.open(pyproject_path, "rb") as f:
            pyproject_content = toml_load(f)

        dependency = formatter_to_dependency[formatter]
        assert (
            dependency in pyproject_content["tool"]["poetry"]["group"]["dev"]["dependencies"]
        ) is (expected is not None)
        tasks_path = result.project.join("tasks.py")
        tasks_content = tasks_path.read()
        if expected is not None:
            assert expected in tasks_content
        else:
            assert "black --check" not in tasks_content
            assert "ruff format" not in tasks_content


@pytest.mark.parametrize(
    "command",
    [
        "poetry run invoke lint",
        "poetry run invoke docs --no-launch",
    ],
)
def test_bake_and_run_and_invoke(cookies, command):
    """Run the unit tests of a newly-generated project using invoke's tasks."""
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        return_code = run_inside_dir(command, str(result.project))
        assert return_code == 0, f"'{command}' failed with return code {return_code}"
