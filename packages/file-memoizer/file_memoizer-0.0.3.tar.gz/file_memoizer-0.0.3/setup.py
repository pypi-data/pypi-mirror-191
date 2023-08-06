# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_memoizer']

package_data = \
{'': ['*']}

install_requires = \
['cachier>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'file-memoizer',
    'version': '0.0.3',
    'description': 'Store function results across executions using cache files',
    'long_description': '# File Memoizer\n\n[![license](https://img.shields.io/github/license/lordjabez/file-memoizer?color=blue&label=License)](https://opensource.org/licenses/MIT)\n[![PyPi:version](https://img.shields.io/pypi/v/file-memoizer?color=blue&label=PyPI)](https://pypi.org/project/file-memoizer/)\n[![Tests](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/test.yml)\n[![Linter](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/lint.yml)\n[![Security](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/scan.yml)\n[![Release](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml/badge.svg)](https://github.com/lordjabez/file-memoizer/actions/workflows/release.yml)\n\nThis Python package makes it easy to store function results across executions using cache files.\n\n\n## Prerequisites\n\nInstallation is via `pip`:\n\n```bash\npip install file-memoizer\n```\n\n\n## Usage\n\nBasic usage is as follows:\n\n```python3\nimport file_memoizer\n\nfile_memoizer.memoize()\ndef double(n):\n    return 2 * n\n\nclass Arithmetic():\n\n    @staticmethod\n    @file_memoizer.memoize()\n    def triple(n):\n         return 3 * n\n    \n    @file_memoizer.memoize()\n    def multiply(self, x, y):\n        return x * y\n```\n',
    'author': 'Judson Neer',
    'author_email': 'judson.neer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lordjabez/file-memoizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
