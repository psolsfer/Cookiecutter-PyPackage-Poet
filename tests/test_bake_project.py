import datetime
import importlib
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest
import tomli
from click.testing import CliRunner as ClickCliRunner
from cookiecutter.utils import rmtree
from typer.testing import CliRunner as TyperCliRunner

# TODO Implement invoke ("poetry run invoke format --check", "poetry run invoke lint", "poetry run invoke docs --no-launch", "poetry run invoke test"), as in https://github.com/briggySmalls/cookiecutter-pypackage


@contextmanager
def inside_dir(dirpath):
    """Execute code from inside the given directory.

    :param dirpath: String, path of the directory the command is being run.
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

    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the exit status.

    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output."""
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies."""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = Path(project_path) / "src" / project_slug
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        # assert "python_boilerplate" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files

        assert result.project.join("src/python_boilerplate").isdir()


def test_bake_and_run_tests(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        run_inside_dir("poetry run pytest", str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_withspecialchars_and_run_tests(cookies):
    """Ensure that a `full_name` with double quotes does not break pyproject.toml."""
    with bake_in_temp_dir(cookies, extra_context={"full_name": 'name "quote" name'}) as result:
        assert result.project.isdir()
        run_inside_dir("poetry run pytest", str(result.project)) == 0


def test_bake_with_apostrophe_and_run_tests(cookies):
    """Ensure that a `full_name` with apostrophes does not break pyproject.toml."""
    with bake_in_temp_dir(cookies, extra_context={"full_name": "O'connor"}) as result:
        assert result.project.isdir()
        run_inside_dir("poetry run pytest", str(result.project)) == 0


def test_bake_without_author_file(cookies):
    with bake_in_temp_dir(cookies, extra_context={"create_author_file": "n"}) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "AUTHORS.md" not in found_toplevel_files
        doc_files = [f.basename for f in result.project.join("docs").listdir()]
        assert "authors.md" not in doc_files

        # Assert there are no spaces in the toc tree
        # docs_index_path = result.project.join("docs/index.md")
        # with Path.open(str(docs_index_path)) as index_file:
        #     assert "contributing\n   history" in index_file.read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir("make help", str(result.project))
            assert b"check code coverage quickly with the default Python" in output


def test_bake_selecting_license(cookies):
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
            # with bake_in_temp_dir(
            #     cookies, extra_context={"open_source_license": license_name}
            # ) as result:
            assert target_string in result.project.join("LICENSE").read()
            assert license_name in result.project.join("pyproject.toml").read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"open_source_license": "Not open source"}
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.md").read()


def test_using_pytest(cookies):
    with bake_in_temp_dir(cookies, extra_context={"use_pytest": "y"}) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import pytest" in "".join(lines)
        # Test the new pytest target
        run_inside_dir("pytest", str(result.project)) == 0


def test_not_using_pytest(cookies):
    context = {"use_pytest": "n"}
    with bake_in_temp_dir(cookies, extra_context=context) as result:
        assert result.project.isdir()
        test_file_path = result.project.join("tests/test_python_boilerplate.py")
        lines = test_file_path.readlines()
        assert "import unittest" in "".join(lines)
        assert "import pytest" not in "".join(lines)


def test_bake_with_no_console_script(cookies):
    context = {"command_line_interface": "No command-line interface"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" not in found_project_files

    pyproject_path = os.path.join(project_path, "pyproject.toml")
    with open(pyproject_path, "r") as pyproject_file:
        assert "[tool.poetry.scripts]" not in pyproject_file.read()


def test_bake_with_console_script_files(cookies):
    context = {"command_line_interface": "Click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    pyproject_path = os.path.join(project_path, "pyproject.toml")
    with open(pyproject_path, "r") as pyproject_file:
        assert "[tool.poetry.scripts]" in pyproject_file.read()


def test_bake_with_typer_console_script_files(cookies):
    context = {"command_line_interface": "Typer"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    pyproject_path = os.path.join(project_path, "pyproject.toml")
    with open(pyproject_path, "r") as pyproject_file:
        assert "[tool.poetry.scripts]" in pyproject_file.read()


def test_bake_with_argparse_console_script_files(cookies):
    context = {"command_line_interface": "Argparse"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    found_project_files = os.listdir(project_dir)
    assert "cli.py" in found_project_files

    pyproject_path = os.path.join(project_path, "pyproject.toml")
    with open(pyproject_path, "r") as pyproject_file:
        assert "[tool.poetry.scripts]" in pyproject_file.read()


def test_bake_with_console_script_cli(cookies):
    context = {"command_line_interface": "Click"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = ClickCliRunner()
    noarg_result = runner.invoke(cli.main)
    assert noarg_result.exit_code == 0
    noarg_output = " ".join(["Replace this message by putting your code into", project_slug])
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


def test_bake_with_typer_console_script_cli(cookies):
    context = {"command_line_interface": "Typer"}
    result = cookies.bake(extra_context=context)
    project_path, project_slug, project_dir = project_info(result)
    module_path = os.path.join(project_dir, "cli.py")
    module_name = ".".join([project_slug, "cli"])
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    runner = TyperCliRunner()
    noarg_result = runner.invoke(cli.app)  # Change 'main' to 'app' for Typer
    assert noarg_result.exit_code == 0
    noarg_output = " ".join(["Replace this message by putting your code into", project_slug])
    assert noarg_output in noarg_result.output
    help_result = runner.invoke(cli.app, ["--help"])  # Change 'main' to 'app' for Typer
    assert help_result.exit_code == 0
    assert "Show this message" in help_result.output


# FIXME This test doesn't work: "FAILED tests/test_bake_project.py::test_bake_with_argparse_console_script_cli - AttributeError: 'function' object has no attribute 'name'"
# def test_bake_with_argparse_console_script_cli(cookies):
#     context = {"command_line_interface": "Argparse"}
#     result = cookies.bake(extra_context=context)
#     project_path, project_slug, project_dir = project_info(result)
#     module_path = os.path.join(project_dir, "cli.py")
#     module_name = ".".join([project_slug, "cli"])
#     spec = importlib.util.spec_from_file_location(module_name, module_path)
#     cli = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(cli)
#     runner = ClickCliRunner()
#     noarg_result = runner.invoke(cli.main)
#     assert noarg_result.exit_code == 0
#     noarg_output = " ".join(["Replace this message by putting your code into", project_slug])
#     assert noarg_output in noarg_result.output
#     help_result = runner.invoke(cli.main, ["--help"])
#     assert help_result.exit_code == 0
#     assert "Show this message" in help_result.output


@pytest.mark.parametrize(
    "formatter,expected", [("Black", "black --check"), ("Ruff-format", "ruff"), ("No", None)]
)
def test_formatter(cookies, formatter, expected):
    formatter_to_dependency = {"Black": "black", "Ruff-format": "ruff", "No": None}

    with bake_in_temp_dir(cookies, extra_context={"formatter": formatter}) as result:
        assert result.project.isdir()
        pyproject_path = result.project.join("pyproject.toml")
        with Path.open(pyproject_path, "rb") as f:
            pyproject_content = tomli.load(f)

        # FIXME This assert will fail for ruff-format, as the dependency is "ruff", not "ruff-format"
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
