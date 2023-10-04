# Cookiecutter PyPackage Poet

----

| | |
| --- | :---: |
| **Docs** | [![Documentation Status](<https://readthedocs.org/projects/cookiecutter-pypackage-poet/badge/?version=latest> 'Documentation Status')](https://cookiecutter-pypackage-poet.readthedocs.io/en/latest/) |
| **GitHub** | [![Cookiecutter PyPackage Poet project](https://img.shields.io/badge/GitHub-Cookiecutter%20PyPackage%20Poet-blue.svg)](<https://github.com/psolsfer/cookiecutter-pypackage-poet>) [![Forks](https://img.shields.io/github/forks/psolsfer/cookiecutter-pypackage-poet.svg)](<https://github.com/psolsfer/cookiecutter-pypackage-poet>) [![Stars](https://img.shields.io/github/stars/psolsfer/cookiecutter-pypackage-poet.svg)](<https://github.com/psolsfer/cookiecutter-pypackage-poet>) [![Issues](https://img.shields.io/github/issues/psolsfer/cookiecutter-pypackage-poet.svg)](<https://github.com/psolsfer/cookiecutter-pypackage-poet>)
| **Code style** | [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - Ruff formatter](https://img.shields.io/badge/Ruff%20Formatter-checked-blue.svg)](https://github.com/astral-sh/ruff) [![types - Mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
| **License** | [![License - BSD-3-Clause](<https://img.shields.io/pypi/l/cookiecutter-pypackage-poet.svg>)](<https://spdx.org/licenses/BSD-3-Clause.html>) |

[Cookiecutter] / [Cruft] template for a Python package, based on [audreyfeldroy]
and [radix-ai] Cookiecutter packages.

## Features

### Project Setup and Management

- [Cruft]: Keeps the project templates up-to-date
- [Poetry]: A tool for dependency management and packaging in Python
- Auto-release to [PyPi] when you push a new tag to main branch (optional)

### Code Quality Assurance

- [Ruff] and [Black]: Ensure your code is clean and adheres to style guidelines with automated code linting and formatting.
- [Pre-commit]: Managing and maintaining multi-language pre-commit hooks to ensure code quality
- Static type checking with [Mypy] and data validation using [Pydantic]'s type annotations
- Automatic check for dependency updates with [Dependabot]

### Testing

- Testing setup with ``unittest`` and ``pytest``
- [tox] testing: Setup to easily test for Python 3.10 and 3.11
- Test coverage with [Coverage.py]

### Documentation

- Ready-to-go setup documentation with [MkDocs]' theme [Material for MkDocs] and [PyMdown Extensions].
- Hosting of documentation in [Read the Docs] or [Gihub Pages].

### Versioning and Release Notes

- [Commitizen]: Streamline your versioning workflow with semantic versioning and automatic changelog generation.
- Automated release notes drafting process as pull requests are merged into master with [Release Drafter].

### Command Line Interface

- Optional CLI using Click, Typer or argparse.

### Development Tasks

- Development tasks (lint, format, test, etc) wrapped up in a python CLI with [Invoke].

## Usage

For a brief tutorial, refer to the refer to the [Tutorial](docs/tutorial.md) section of the documentation.

The prompts that need to be filled during the creation of the package are described in [Prompts](docs/prompts.md).

## Updating a project

An existing project can be updated to the latest template using:

```bash linenums="0"
cruft update
```

## Alternative templates

Any of the following alternatives is most mature than the current template, and recommended to use:

- [audreyfeldroy/cookiecutter-pypackage]: The original template from which this was forked. It also includes a detailed list of [alternative templates].
- [briggySmalls/cookiecutter-pypackage]: A fork of [audreyfeldroy/cookiecutter-pypackage] using [Poetry] for neat package management and deployment, with linting, formatting, no makefiles and more.
- [TezRomacH/python-package-template]: Cookiecutter template that combines state-of-the-art libraries and best development practices for Python.
- [radix-ai/poetry-cookiecutter]: A modern Cookiecutter template for scaffolding Python packages and apps.

## Credit

The following templates were used as basis and inspiration for the creation of some parts of this template:

- Initial template forked from [audreyfeldroy/cookiecutter-pypackage].
- Implementation of [Poetry] is based in the templates [TezRomacH/python-package-template] and [radix-ai/poetry-cookiecutter].
- Implementation of [Invoke] is based in [briggySmalls/cookiecutter-pypackage].
- Use of release drafter, dependabot, and print instructions after the template is created: [TezRomacH/python-package-template].

[alternative templates]: https://github.com/audreyfeldroy/cookiecutter-pypackage#similar-cookiecutter-templates
[audreyfeldroy/cookiecutter-pypackage]: https://github.com/audreyfeldroy/cookiecutter-pypackage
[briggySmalls/cookiecutter-pypackage]: https://github.com/briggySmalls/cookiecutter-pypackage
[radix-ai/poetry-cookiecutter]: https://github.com/radix-ai/poetry-cookiecutter
[TezRomacH/python-package-template]: https://github.com/TezRomacH/python-package-template

[Black]: https://black.readthedocs.io/en/stable/
[Coverage.py]: https://coverage.readthedocs.io/
[Commitizen]: https://commitizen-tools.github.io/commitizen/
[Cookiecutter]: <https://github.com/cookiecutter/cookiecutter>
[Cruft]: <https://github.com/cruft/cruft>
[Dependabot]: https://github.com/marketplace/actions/release-drafter
[Invoke]: https://www.pyinvoke.org/
[Material for MkDocs]: https://squidfunk.github.io/mkdocs-material/
[MkDocs]: https://www.mkdocs.org/
[Mypy]: https://mypy.readthedocs.io/en/stable/
[Poetry]: https://python-poetry.org/
[Pydantic]: https://docs.pydantic.dev
[Pre-commit]: https://pre-commit.com/
[Read the Docs]: https://readthedocs.org
[Release Drafter]: https://github.com/marketplace/actions/release-drafter
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions
[PyPi]: https://pypi.org/
[Ruff]: https://docs.astral.sh/ruff/
[tox]: https://tox.wiki/
