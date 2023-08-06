# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toml_argparse']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'types-toml>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'toml-argparse',
    'version': '0.0.1a0',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# toml-argparse\n\n[![Release](https://img.shields.io/github/v/release/florianmahner/toml-argparse)](https://img.shields.io/github/v/release/florianmahner/toml-argparse)\n[![Build status](https://img.shields.io/github/actions/workflow/status/florianmahner/toml-argparse/main.yml?branch=main)](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml?query=branch%3Amain)\n![example workflow](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml/badge.svg)\n[![codecov](https://codecov.io/gh/florianmahner/toml-argparse/branch/main/graph/badge.svg)](https://codecov.io/gh/florianmahner/toml-argparse)\n[![License](https://img.shields.io/github/license/florianmahner/toml-argparse)](https://img.shields.io/github/license/florianmahner/toml-argparse)\n![code style](https://img.shields.io/badge/code%20style-black-black)\n\n\n\ntoml-argparse is a python library and command-line-tool that allows you to use TOML configuration files with the argparse module. It provides a simple and convenient way to handle configuration for your python scripts, leveraging the strengths of both TOML and argparse.\n\n## Installation\n\nYou can install the library using pip\n\n```bash\npip install toml-argparse\n```\n\n\n\n## Usage\n\nUsing toml-argparse is straightforward and requires only a few extra steps compared to using argparse alone. You first define your configuration options in a TOML file, then use the [toml_argparse.ArgumentParser](https://github.com/florianmahner/toml-argparse/blob/main/toml_argparse/argparse.py) to add those options to your argparse argument parser. \n\n\n### Basic Example\n[TOML](https://toml.io/en/) files usually come in the following form:\n\n```toml\n# This is a TOML File\n\n# These are parameters not part of a section\nfoo = 10\nbar = "hello"\n\n# This is a parameter that belongs to a section\n[general]\nfoo = 42\n```\n\nSay we want to use the fields from the TOML file also for our python project. To do this we would create an `ArgumentParser` as usual:\n\n```python\nfrom toml_argparse import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("--foo", type-int, default=0)\nparser.add_argumetn("--bar", type=str, default="")\nparser.parse_args()\n```\n\nThis is just a very simple example with two arguments. For large projects with a lot of hyperparameters the number of arguments usually increases quickly. In this case, we can now easily parse parameters through the TOML file from the command-line:\n\n\n```bash\npython experiment.py --config "example.toml"\n```\nThis will replace our argparse defaults with the ones specified in the toml file.\n\n\n## Contributing\n\nPlease have a look at the contribution guidlines in `Contributing.rst`.\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'florianmahner',
    'author_email': 'fflorian.mahner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/florianmahner/toml-argparse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
