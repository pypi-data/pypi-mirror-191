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
    'version': '0.0.3',
    'description': 'This is a template repository for Python projects that use Poetry for their dependency management.',
    'long_description': '# toml-argparse\n\n[![Release](https://img.shields.io/github/v/release/florianmahner/toml-argparse)](https://img.shields.io/github/v/release/florianmahner/toml-argparse)\n[![Build status](https://img.shields.io/github/actions/workflow/status/florianmahner/toml-argparse/main.yml?branch=main)](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml?query=branch%3Amain)\n![example workflow](https://github.com/florianmahner/toml-argparse/actions/workflows/main.yml/badge.svg)\n[![codecov](https://codecov.io/gh/florianmahner/toml-argparse/branch/main/graph/badge.svg)](https://codecov.io/gh/florianmahner/toml-argparse)\n[![License](https://img.shields.io/github/license/florianmahner/toml-argparse)](https://img.shields.io/github/license/florianmahner/toml-argparse)\n![code style](https://img.shields.io/badge/code%20style-black-black)\n\n\ntoml-argparse is a Python library and command-line tool that allows you to use [TOML](https://toml.io/en/) configuration files in conjunction with the [argparse module](https://docs.python.org/3/library/argparse.html). It provides a simple and convenient way to handle your python projects, leveraging the strengths of both TOML and argparse.\n\n\n# Table of Contents\n1. [Installation](#installation)\n2. [Usage](#usage)\n    1. [Basic Example](#basic-example)\n    2. [Extended Example](#extended-example)\n5. [Contributing](#contributing)\n\n\n## Installation\n\nYou can install the library using pip\n\n```bash\npip install toml-argparse\n```\n\n\n## Usage\n\nUsing toml-argparse is straightforward and requires only a few extra steps compared to using argparse alone.\n\n### Basic Example\n\nYou first define your configuration options in a TOML file. TOML files are highly flexible and include a lot of native types. Have look [here](https://toml.io/en/v1.0.0) for an extensive list.  TOML files usually come in the following form:\n\n```toml\n# This is a very basic TOML file\nfoo = 10\nbar = "hello"\n```\n\nAt the core of this module is the  [TOML ArgumentParser](https://github.com/florianmahner/toml-argparse/blob/main/toml_argparse/argparse.py), a simple wrapper of the original argparse module. To use the TOML arguments for our project, we we would create an `ArgumentParser` as usual:\n\n```python\nfrom toml_argparse import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("--foo", type-int, default=0)\nparser.add_argumetn("--bar", type=str, default="")\nparser.parse_args()\n```\n\nThis is just a simple example with two arguments. But for larger projects with many hyperparameters, the number of arguments can quickly grow, and the TOML file provides an easy way to collect and store different hyperparameter configurations. Every TOML ArgumentParser has a `config` argument defined that we can pass using the following command-line syntax:\n\n```bash\npython experiment.py --config "example.toml"\n```\n\nThis will replace the default values from the ArgumentParser with the TOML values.\n\n### Extended Example\n\nTOML files have the ability to separate arguments into different sections (called `tables`), which are represented by nested dictionaries:\n\n```toml\n# This is a TOML File\n\n# Parameters without a prededing [] are not part of a table (called root-table)\nfoo = 10\nbar = "hello"\n\n# These arguments are part of the table [general]\n[general]\nfoo = 20\n\n# These arguments are part of the table [root]\n[root]\nbar = "hey"\n```\n\nIf we would load this TOML file as usual this would return a dict `{"foo": 10, "bar": "hello", "general": {"foo": 20}, "root" : {"bar": "hey"}}`. Note that `foo` and `bar` are overloaded and defined twice. To specify the values we wish to take each TOML ArgumentParser has two arguments defined:\n\n1. `table`\n2. `root-table`\n\nWe can use these directly from the command-line:\n\n```bash\npython experiment.py --config "example.toml" --table "general"\n```\n\nIn this case the `root-table` is not defined. In this case the arguments at the top of the file without a table are taken and parsing would return the following dict `{"foo": 20, "bar": "hello"}`. Note that `table` arguments override arguments from the `root-table`. \n\nWe can also specify the root-table:\n\n```bash\npython experiment.py --config "example.toml" --table "general" --root-table "root"\n```\n\nwhich would return the following dict `{"foo: 20", "bar": "hey"}` and override the arguments from the top of the TOML file.\n\nIn general, we have the following hierarchy of arguments:\n1. Arguments passed through the command line are selected over TOML\n           arguments, even if both are passed\n2. Arguments from the TOML file are preferred over the default arguments\n3. Arguments from the TOML with a section override the arguments without a section\n\nThis means that we can also override arguments in the TOML file from the command-line:\n\n```bash\npython experiment.py --config "example.toml" --table "general" --foo 100\n```\n\n\n## Contributing\n\nPlease have a look at the contribution guidlines in `Contributing.rst`.\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
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
