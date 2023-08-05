# flake8-import-as-module

<p align="center">
  <img alt="" src="https://raw.githubusercontent.com/joaopalmeiro/flake8-import-as-module/main/assets/logo_round.png" width="100" height="100" />
</p>

[![PyPI](https://img.shields.io/pypi/v/flake8-import-as-module.svg)](https://pypi.org/project/flake8-import-as-module/)

A [Flake8](https://flake8.pycqa.org/) plugin to check if specific packages are imported as modules.

## Installation

Via [Pipenv](https://pipenv.pypa.io/):

```bash
pipenv install --dev flake8 flake8-import-as-module
```

## Flake8 codes

| Package                                 | Code  | Description                                                                          |
| --------------------------------------- | ----- | ------------------------------------------------------------------------------------ |
| [Altair](https://altair-viz.github.io/) | IM001 | `from altair import ...` is unconventional. `altair` should be imported as a module. |
| [pandas](https://pandas.pydata.org/)    | IM002 | `from pandas import ...` is unconventional. `pandas` should be imported as a module. |

## References

- https://docs.python.org/3.7/tutorial/modules.html
- https://stackoverflow.com/a/49072655
- https://github.com/marcgibbons/flake8-datetime-import
- https://github.com/joaopalmeiro/flake8-import-conventions
- https://github.com/asottile/flake8-2020

## Development

```bash
poetry install --with dev
```

```bash
poetry shell
```

```bash
pytest tests/ -v
```

Copy the output of the following script and paste it in the [Flake8 codes](#flake8-codes) section:

```bash
python gen_table.py
```

If changes are not reflected in VS Code after changing something in the package, close it and open it again.

## Deployment

```bash
poetry check
```

```bash
poetry version minor
```

or

```bash
poetry version patch
```

Commit the change in the `pyproject.toml` file.

```bash
git tag
```

```bash
git tag "v$(poetry version --short)"
```

```bash
git push origin "v$(poetry version --short)"
```
