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
    'version': '0.0.2',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# toml-argparse\n\n[![Release](https://img.shields.io/github/v/release/florianmahner/toml-argparse)](https://img.shields.io/github/v/release/florianmahner/toml-argparse)\n[![Build status](https://img.shields.io/github/actions/workflow/status/florianmahner/toml-argparse/main.yml?branch=main)](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml?query=branch%3Amain)\n![example workflow](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml/badge.svg)\n[![codecov](https://codecov.io/gh/florianmahner/toml-argparse/branch/main/graph/badge.svg)](https://codecov.io/gh/florianmahner/toml-argparse)\n[![License](https://img.shields.io/github/license/florianmahner/toml-argparse)](https://img.shields.io/github/license/florianmahner/toml-argparse)\n![code style](https://img.shields.io/badge/code%20style-black-black)\n\n\n\ntoml-argparse is a python library and command-line-tool that allows you to use [TOML](https://toml.io/en/) configuration files with the [argparse](https://docs.python.org/3/library/argparse.html) module. It provides a simple and convenient way to handle configuration for your python scripts, leveraging the strengths of both TOML and argparse.\n\n## Installation\n\nYou can install the library using pip\n\n```bash\npip install toml-argparse\n```\n\n\n## Usage\n\nUsing toml-argparse is straightforward and requires only a few extra steps compared to using argparse alone. You first define your configuration options in a TOML file, then use the [TOML ArgumentParser](https://github.com/florianmahner/toml-argparse/blob/main/toml_argparse/argparse.py). \n\n### Basic Example\n\n[TOML](https://toml.io/en/) files usually come in the following form:\n\n```toml\n# This is a very basic TOML file without a section\nfoo = 10\nbar = "hello"\n```\n\n\nThe [TOML ArgumentParser](https://github.com/florianmahner/toml-argparse/blob/main/toml_argparse/argparse.py) is a simple wrapper of the original argparse module. It therefore provides the exact same fumctionality. To use the TOML arguments for our project, we we would create an `ArgumentParser` as usual:\n\n```python\nfrom toml_argparse import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("--foo", type-int, default=0)\nparser.add_argumetn("--bar", type=str, default="")\nparser.parse_args()\n```\n\nThis is just a very simple example with two arguments. However, for large projects with a lot of hyperparameters the number of arguments usually increases quickly and the TOML file provides an easy way to collect and store different hyperparameter configurations. We can do this by parsing  parameters from the TOML file from the command-line:\n\n```bash\npython experiment.py --config "example.toml"\n```\n\n### Extended Example\n\nTOML files have the power to separate arguments into different sections that are represented by nested dictionaries:\n\n```toml\n# This is a TOML File\n\n# These are parameters not part of a section\nfoo = 10\nbar = "hello"\n\n[general]\nfoo = 20\n```\n\nIf we would load this TOML file as usual this would return a dict {"foo": 10, "bar": "hello", "general": {"foo": 20}. Note that foo is overloaded and defined twice. We can also load arguments from a specific section through the corresponding keyword `section`:\n\n```bash\npython experiment.py --config "example.toml" --section "general"\n```\n\nThis would return the following dict {"foo": 20, "bar": "hello"}. Note that section arguments override arguments without a section.\n\nIn general, we have the following hierarchy of arguments:\n1. Arguments passed through the command line are selected over TOML\n           arguments, even if both are passed\n2. Arguments from the TOML file are preferred over the default arguments\n3. Arguments from the TOML with a section override the arguments without a section\n\nThis means that we can also override arguments in the TOML file from the command-line:\n\n\n```bash\npython experiment.py --config "example.toml" --section "general" --foo 100\n```\n\n\n## Contributing\n\nPlease have a look at the contribution guidlines in `Contributing.rst`.\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
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
