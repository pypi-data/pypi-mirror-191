# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pretty_history']

package_data = \
{'': ['*']}

install_requires = \
['browserexport>=0.2.7,<0.3.0']

entry_points = \
{'console_scripts': ['prettyhist = pretty_history.main:main']}

setup_kwargs = {
    'name': 'pretty-history',
    'version': '1.0.2',
    'description': 'Generate a pretty view of your browser history from a JSON export',
    'long_description': '# pretty-history\n',
    'author': 'Arjun Patel',
    'author_email': 'relay-git-1LKQ1GqLp0Nn4@aspatel.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/apatel762/pretty-history',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
