# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sparkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sparkit',
    'version': '0.0.1',
    'description': 'A package for PySpark utility functions.',
    'long_description': '<p align="center">\n<img src="https://raw.githubusercontent.com/estripling/sparkit/main/docs/source/_static/logo.png" width="180" alt="The sparkit logo.">\n</p>\n\n<p align="center">\n<a href="https://pypi.org/project/sparkit"><img alt="pypi" src="https://img.shields.io/pypi/v/sparkit"></a>\n<a href="https://readthedocs.org/projects/sparkit/?badge=latest"><img alt="docs" src="https://readthedocs.org/projects/sparkit/badge/?version=latest"></a>\n<a href="https://github.com/estripling/sparkit/actions/workflows/ci.yml"><img alt="ci status" src="https://github.com/estripling/sparkit/actions/workflows/ci.yml/badge.svg?branch=main"></a>\n<a href="https://codecov.io/gh/estripling/sparkit"><img alt="coverage" src="https://codecov.io/github/estripling/sparkit/coverage.svg?branch=main"></a>\n<a href="https://github.com/estripling/sparkit/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/pypi/l/sparkit"></a>\n</p>\n\n## About\n\nA package for PySpark utility functions:\n\n- [Documentation](https://sparkit.readthedocs.io/en/stable/index.html)\n- [Example usage](https://sparkit.readthedocs.io/en/stable/example.html)\n- [API Reference](https://sparkit.readthedocs.io/en/stable/autoapi/sparkit/index.html)\n\n## Installation\n\n`sparkit` is available on [PyPI](https://pypi.org/project/sparkit/) for Python 3.8+:\n\n```console\npip install sparkit\n```\n\n## Examples\n\n- TODO\n\n## Contributing to sparkit\n\nYour contribution is greatly appreciated!\nSee the following links to help you get started:\n\n- [Contributing Guide](https://sparkit.readthedocs.io/en/latest/contributing.html)\n- [Developer Guide](https://sparkit.readthedocs.io/en/latest/developers.html)\n- [Contributor Code of Conduct](https://sparkit.readthedocs.io/en/latest/conduct.html)\n\n## License\n\n`sparkit` was created by sparkit Developers.\nIt is licensed under the terms of the BSD 3-Clause license.\n',
    'author': 'sparkit Developers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/estripling/sparkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
