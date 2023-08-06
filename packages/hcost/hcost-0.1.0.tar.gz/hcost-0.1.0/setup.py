# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hcost']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'hcost',
    'version': '0.1.0',
    'description': 'A simple program to calculate the heating costs based on (semi-) yearly oil deliveries.',
    'long_description': '# hcost\n\n## Motivation\n\nA package which calculates the proportional heating costs, based on different heating deliveries.\n\n## Installation\n\n```\npip install hcost\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/hcost',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
