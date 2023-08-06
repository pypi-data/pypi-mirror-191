# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synthesize']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3',
 'identify>=2.5.17',
 'lark>=1.1.5',
 'networkx>=3.0',
 'pydantic>=1.10.4',
 'pyyaml>=6.0',
 'rich>=13.3.0',
 'typer>=0.7.0',
 'watchfiles>=0.18.1']

entry_points = \
{'console_scripts': ['synth = synthesize.cli:cli']}

setup_kwargs = {
    'name': 'synthesize',
    'version': '0.0.2',
    'description': 'A flexible concurrent command runner.',
    'long_description': '# Synthesize\n\n[![PyPI](https://img.shields.io/pypi/v/synthesize)](https://pypi.org/project/synthesize)\n[![PyPI - License](https://img.shields.io/pypi/l/synthesize)](https://pypi.org/project/synthesize)\n[![Docs](https://img.shields.io/badge/docs-exist-brightgreen)](https://www.synth.how)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/synthesize/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/synthesize/main)\n[![codecov](https://codecov.io/gh/JoshKarpel/synthesize/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/synthesize)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/synthesize)](https://github.com/JoshKarpel/synthesize/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/synthesize)](https://github.com/JoshKarpel/synthesize/pulls)\n',
    'author': 'Josh Karpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
