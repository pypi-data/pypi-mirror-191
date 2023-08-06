# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zana', 'zana.common', 'zana.proxy', 'zana.types']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'zana',
    'version': '0.1.5',
    'description': 'general utility functions and types',
    'long_description': '# Python Zana\n\n\n[![PyPi version][pypi-image]][pypi-link]\n[![Supported Python versions][pyversions-image]][pyversions-link]\n[![Build status][ci-image]][ci-link]\n[![Coverage status][codecov-image]][codecov-link]\n\n\nA Python tool kit\n\n\n\n## Installation\n\nInstall from [PyPi](https://pypi.org/project/zana/)\n\n```\npip install zana\n```\n\n## Documentation\n\nFull documentation is available [here][docs-link].\n\n\n\n## Production\n\n__This package is still in active development and should not be used in production environment__\n\n\n\n\n[docs-link]: https://python-zana.github.io/zana/\n[pypi-image]: https://img.shields.io/pypi/v/zana.svg?color=%233d85c6\n[pypi-link]: https://pypi.python.org/pypi/zana\n[pyversions-image]: https://img.shields.io/pypi/pyversions/zana.svg\n[pyversions-link]: https://pypi.python.org/pypi/zana\n[ci-image]: https://github.com/python-zana/zana/actions/workflows/workflow.yaml/badge.svg?event=push&branch=main\n[ci-link]: https://github.com/python-zana/zana/actions?query=workflow%3ACI%2FCD+event%3Apush+branch%3Amaster\n[codecov-image]: https://codecov.io/gh/python-zana/zana/branch/main/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/python-zana/zana\n\n\nSee this release on GitHub: [v0.1.5](https://github.com/python-zana/zana/releases/tag/0.1.5)\n',
    'author': 'David Kyalo',
    'author_email': 'davidmkyalo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/python-zana/zana',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
