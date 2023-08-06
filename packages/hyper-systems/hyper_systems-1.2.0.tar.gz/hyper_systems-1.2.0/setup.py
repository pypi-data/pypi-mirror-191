# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyper_systems', 'hyper_systems.devices', 'hyper_systems.http']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hyper-systems',
    'version': '1.2.0',
    'description': 'Python SDK for interacting with the Hyper.systems platform.',
    'long_description': '# hyper-python-sdk\n\nPython SDK for interacting with the Hyper.systems platform.\n\nCheck [here](./antora/modules/ROOT/pages/index.adoc) for usage and other documentation.\n\n**Pypi.org:**\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/hyper-systems.svg)](https://pypi.org/project/hyper-systems)\n\n## Installing\n\nInstall the latest version globally using pip:\n\n```shell\npip install -U hyper-systems\n```\n\n### Adding as a dependency to your project\n\nAdd to `requirements.txt` for pip:\n\n```shell\necho "hyper-systems==1.2.0" >> requirements.txt\n```\n\nConsider using [venv](https://docs.python.org/3/tutorial/venv.html), if you want to have an isolated environment for your project with pip.\n\nAlternatively, install with poetry:\n\n```shell\npoetry add "hyper-systems==1.2.0"\n```\n\n### Installing the latest development version of the package globally\n\n```shell\n$ pip install -U git+https://github.com/hyper-systems/hyper-python-sdk.git@master\n```\n\n## Using this repo for development\n\nThis repo uses [poetry](https://python-poetry.org/) (please check the [docs](https://python-poetry.org/docs/)) for development and building. It is currentlu set up to create a `.venv` directory in the root of this project on install.\n\n\nInstalling the environment:\n\n```shell\n$ poetry install\n```\n\n### Shell usage\n\nAfter installing you can use the environment created with poetry, for example to:\n\n- update the environment:\n\n```shell\n$ poetry update\n```\n\n- execute scripts:\n\n```shell\n$ poetry run tests/test_devices.py\n```\n\n### VSCode\n\nYou can also use the environment in VSCode by opening one of the python files in this repo and selecting the poetry python interpreter in the bottom left corner (`(\'.venv\': poetry)`). You then reload the VSCode window (or open and close VSCode) and VSCode should be now using the `.venv` environment created by poetry.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hyper.systems',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
