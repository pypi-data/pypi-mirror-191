<div align="center">

<img src="https://i.imgur.com/jjnYRTV.png" title="tethys">

[![Tests](https://github.com/pcsagan/tethys/actions/workflows/tests.yml/badge.svg)](https://github.com/pcsagan/tethys/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/tethys-template.svg?label=PyPI)](https://pypi.org/project/tethys-template/)
[![Code of conduct](https://img.shields.io/badge/Code%20of%20conduct-welcoming-blue)](https://github.com/pcsagan/tethys/blob/main/CODE_OF_CONDUCT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/pcsagan/tethys/blob/main/LICENSE)

</div>

## Using this template

1. Create a new repository using Github's template interface, or run the following commands:
    ```shell
    git clone https://github.com/pcsagan/tethys <your_package_name>
    cd <your_package_name>
    rm -rf .git
    git init .
    ```
2. Find and replace all instances of `tethys` and `tethys-template` with your package name
    - Your project name can match your package name. The name `tethys-template` was required because`tethys` already exists on PyPI
3. Update `pyproject.toml` to reflect its new author and requirements
    - Update the [Security Policy](https://github.com/pcsagan/tethys/blob/main/SECURITY.md) and the [Code of Conduct](https://github.com/pcsagan/tethys/blob/main/CODE_OF_CONDUCT.md) with your e-mail address
    - Set the version to a value that hasn't already been published to [PyPI](https://pypi.org) (and [TestPyPI](https://test.pypi.org))
    - List of [Classifiers](https://pypi.org/classifiers/)
    - Configuration for [mypy](https://mypy.readthedocs.io/en/stable/config_file.html)
4. Update `tox.ini` to build the desired testing environments
    - Configuration for [black](https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html)
    - Configuration for [flake8](https://flake8.pycqa.org/en/latest/user/configuration.html)    
    - Configuration for [pycodestyle](https://pycodestyle.pycqa.org/en/latest/intro.html#configuration)
    - Configuration for [pydocstyle](http://www.pydocstyle.org/en/stable/usage.html#configuration-files)    
    - Configuration for [pytest](https://docs.pytest.org/en/7.1.x/reference/customize.html#tox-ini)
    - Configuration for [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/tox.html)
5. Update `cli.py` to customize the command line interface
    - Documentation for [click](https://click.palletsprojects.com/)
    - The entry point is defined in the project.scripts table in the `pyproject.toml` file
6. Update `.git/workflows/tests.yaml` to specify the various operating systems and python versions used for testing
7. Install your package dependencies into your development environment
    - Install the package locally in editable mode using the command:
        ```shell
        pip install -e .
        ```
    - Install the package locally along with all testing libraries used by `tox` with the command:
        ```shell
        pip install -r requirements.txt
        ```
7. Add your code to the package while regularly committing your changes to your Github repository
8. Add your tests to the `tests` directory
9. Test your package using `tox`
    - Run all tasks in their own environments using the command:
        ```shell
        tox
        ```
    - Run specific tasks using `tox` with the `-e` flag:
        ```shell
        tox -e black
        tox -e docs
        tox -e flake8
        tox -e mypy
        tox -e pycodestyle
        tox -e pydocstyle
        tox -e pytest
        tox -e validate-pyproject
        ```
    - If you installed the `requirements.txt` file then you can use testing packages in your local environment:
        ```shell
        black src
        sphinx-apidoc -f -o docs/source src/<my_package_name>
        sphinx-build -b html docs/source docs/build/html
        flake8 src tests
        mypy src
        pycodestyle src
        pydocstyle src
        pytest tests
        ```
10. Register on [PyPI](https://pypi.org) (and [TestPyPI](https://test.pypi.org)) and generate [API tokens](https://pypi.org/help/#apitoken)
11. Add your tokens as a [secret variable](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named `pypi_api_token` and `testpypi_api_token` to your Github repository
12. Manually run the `Publish Test` action to verify that your token and package version are accepted using TestPyPI
13. Manually run the `Publish` action to publish your package on PyPI

## Help

```
Usage: tethys [OPTIONS] COMMAND [ARGS]...

  Tethys is a moon of Saturn.

Options:
  --version  Show the version and exit.
  --debug    Run the command in debug mode.
  --help     Show this message and exit.

Commands:
  data  Print the shared context data to the screen.
  foo   Print the result of calling the foo function to the screen.
```

