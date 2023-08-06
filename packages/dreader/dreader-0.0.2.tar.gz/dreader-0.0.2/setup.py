# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dreader', 'dreader.config_params']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dreader',
    'version': '0.0.2',
    'description': 'Deepdog Reader',
    'long_description': '# dreader - the Deepdog Reader\n\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-green.svg?style=flat-square)](https://conventionalcommits.org)\n[![PyPI](https://img.shields.io/pypi/v/dreader?style=flat-square)](https://pypi.org/project/dreader/)\n[![Jenkins](https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Fdreader%2Fjob%2Fmaster&style=flat-square)](https://jenkins.deepak.science/job/gitea-physics/job/dreader/job/master/)\n![Jenkins tests](https://img.shields.io/jenkins/tests?compact_message&jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Fdreader%2Fjob%2Fmaster%2F&style=flat-square)\n![Jenkins Coverage](https://img.shields.io/jenkins/coverage/cobertura?jobUrl=https%3A%2F%2Fjenkins.deepak.science%2Fjob%2Fgitea-physics%2Fjob%2Fdreader%2Fjob%2Fmaster%2F&style=flat-square)\n![Maintenance](https://img.shields.io/maintenance/yes/2023?style=flat-square)\n\nParses results from deepdog and other utils.\n\n## Getting started\n\n`poetry install` to start locally\n\nCommit using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), and when commits are on master, release with `doo release`.\n',
    'author': 'Deepak',
    'author_email': 'dmallubhotla+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
