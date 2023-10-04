# Installation

----

## Stable release

To install {{ cookiecutter.project_name }}, run this command in your terminal:

=== ":simple-poetry: Poetry (recommended)"

    ```bash linenums="0"
    poetry add {{ cookiecutter.project_slug }}
    ```

    If you don’t have [Poetry] installed, you can refer to the following instructions for [Poetry installation].

=== "pip"

    ```bash linenums="0"
    pip install {{ cookiecutter.project_slug }}
    ```

    If you don't have [pip] installed, this [Python installation guide] can guide
    you through the process.

These are the preferred methods to install {{ cookiecutter.project_name }}, as it will always install the most recent stable release.

## From sources

The sources for {{ cookiecutter.project_name }} can be downloaded from the [Github repo].

You can either clone the public repository or download the [tarball].

=== "Cloning"

    ```bash linenums="0"
    git clone git://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
    ```

=== "Tarball"

    ```bash linenums="0"
    curl -OJL https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/main
    ```

Once you have a copy of the source, you can install it with:

```bash linenums="0"
cd {{ cookiecutter.project_slug }}
poetry install
```

This command installs all dependencies as specified in `pyproject.toml` and also creates a virtual environment if one doesn't exist.

[Github repo]: <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}>
[tarball]: <https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/tarball/main/>
