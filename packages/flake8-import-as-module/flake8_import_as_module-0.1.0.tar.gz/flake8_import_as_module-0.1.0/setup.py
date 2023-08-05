# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_import_as_module']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=5']

entry_points = \
{'flake8.extension': ['IM = flake8_import_as_module:Plugin']}

setup_kwargs = {
    'name': 'flake8-import-as-module',
    'version': '0.1.0',
    'description': 'A Flake8 plugin to check if specific packages are imported as modules.',
    'long_description': '# flake8-import-as-module\n\n<p align="center">\n  <img alt="" src="https://raw.githubusercontent.com/joaopalmeiro/flake8-import-as-module/main/assets/logo_round.png" width="100" height="100" />\n</p>\n\n[![PyPI](https://img.shields.io/pypi/v/flake8-import-as-module.svg)](https://pypi.org/project/flake8-import-as-module/)\n\nA [Flake8](https://flake8.pycqa.org/) plugin to check if specific packages are imported as modules.\n\n## Installation\n\nVia [Pipenv](https://pipenv.pypa.io/):\n\n```bash\npipenv install --dev flake8 flake8-import-as-module\n```\n\n## Flake8 codes\n\n| Package                                 | Code  | Description                                                                          |\n| --------------------------------------- | ----- | ------------------------------------------------------------------------------------ |\n| [Altair](https://altair-viz.github.io/) | IM001 | `from altair import ...` is unconventional. `altair` should be imported as a module. |\n| [pandas](https://pandas.pydata.org/)    | IM002 | `from pandas import ...` is unconventional. `pandas` should be imported as a module. |\n\n## References\n\n- https://docs.python.org/3.7/tutorial/modules.html\n- https://stackoverflow.com/a/49072655\n- https://github.com/marcgibbons/flake8-datetime-import\n- https://github.com/joaopalmeiro/flake8-import-conventions\n- https://github.com/asottile/flake8-2020\n\n## Development\n\n```bash\npoetry install --with dev\n```\n\n```bash\npoetry shell\n```\n\n```bash\npytest tests/ -v\n```\n\nCopy the output of the following script and paste it in the [Flake8 codes](#flake8-codes) section:\n\n```bash\npython gen_table.py\n```\n\nIf changes are not reflected in VS Code after changing something in the package, close it and open it again.\n\n## Deployment\n\n```bash\npoetry check\n```\n\n```bash\npoetry version minor\n```\n\nor\n\n```bash\npoetry version patch\n```\n\nCommit the change in the `pyproject.toml` file.\n\n```bash\ngit tag\n```\n\n```bash\ngit tag "v$(poetry version --short)"\n```\n\n```bash\ngit push origin "v$(poetry version --short)"\n```\n',
    'author': 'João Palmeiro',
    'author_email': 'joaopalmeiro@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
