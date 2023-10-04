#!/usr/bin/env python

"""Tests for `{{ cookiecutter.project_name }}` package."""

{% if cookiecutter.use_pytest == 'y' %}
import pytest
{% else %}
import unittest
{%- endif %}
{% if cookiecutter.command_line_interface|lower == 'click' %}
from click.testing import CliRunner
{% elif cookiecutter.command_line_interface|lower == 'typer' %}
from typer.testing import CliRunner
{% endif %}

from {{ cookiecutter.project_slug }} import {{ cookiecutter.project_slug }}
{% if cookiecutter.command_line_interface|lower == 'click' %}
from {{ cookiecutter.project_slug }} import cli
{% elif cookiecutter.command_line_interface|lower == 'typer' %}
from {{ cookiecutter.project_slug }} import app
{% endif %}

{% if cookiecutter.use_pytest == 'y' %}
@pytest.fixture
def response():
    """Sample pytest fixture."""
    # import requests
    # return requests.get('https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}')"""

def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
{% if cookiecutter.command_line_interface|lower == 'click' %}

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{% elif cookiecutter.command_line_interface|lower == 'typer' %}

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(app.main)
    assert result.exit_code == 0
    assert '{{ cookiecutter.project_slug }}.app.main' in result.output
    help_result = runner.invoke(app.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
{% endif %}
{% else %}

class Test{{ cookiecutter.project_slug|title }}(unittest.TestCase):
    """Tests for `{{ cookiecutter.project_slug }}` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
{% if cookiecutter.command_line_interface|lower == 'click' %}

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert '{{ cookiecutter.project_slug }}.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
{% elif cookiecutter.command_line_interface|lower == 'typer' %}

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(app.main)
        assert result.exit_code == 0
        assert '{{ cookiecutter.project_slug }}.cli.app.main' in result.output
        help_result = runner.invoke(app.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
{% endif %}
{% endif %}
