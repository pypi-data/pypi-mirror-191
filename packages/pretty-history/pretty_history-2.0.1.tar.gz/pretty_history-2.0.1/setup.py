# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_history']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'browserexport>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['prettyhist = pretty_history.main:main']}

setup_kwargs = {
    'name': 'pretty-history',
    'version': '2.0.1',
    'description': 'Generate a pretty view of your browser history from a JSON export',
    'long_description': '# pretty-history\n\n[![PyTest](https://github.com/apatel762/pretty-history/actions/workflows/pytest.yml/badge.svg)](https://github.com/apatel762/pretty-history/actions/workflows/pytest.yml) [![PyPi version](https://img.shields.io/pypi/v/browserexport.svg)](https://pypi.python.org/pypi/browserexport) [![Python 3.7|3.8|3.9](https://img.shields.io/pypi/pyversions/browserexport.svg)](https://pypi.python.org/pypi/browserexport) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)\n\nThe `pretty-history` app is a simple Python script that can be run via the command-line, and will generate Markdown files summarising your browser history.\n\n## Installation\n\nInstall from the PyPi repository using `pip`:\n\n```\npip install pretty-history\n```\n\n## Usage\n\nAfter installing the app, run:\n\n```\nprettyhist --help\n```\n\nTo see some instructions for how to use it.\n\n### Example\n\nPretty-format browsing history from Firefox:\n\n```bash\nprettyhist -b firefox\n```\n\nPretty-format browsing history from Firefox, merging with data from Brave Browser:\n\n```bash\nbrowserexport save --browser brave --to .\nbrowserexport merge --json ./*.sqlite > ./history.json\n\nprettyhist -b firefox -f ./history.json\n```\n\n## References\n\n1. [seanbreckenridge/browserexport](https://github.com/seanbreckenridge/browserexport)\n',
    'author': 'Arjun Patel',
    'author_email': 'relay-git-1LKQ1GqLp0Nn4@aspatel.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/apatel762/pretty-history',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
