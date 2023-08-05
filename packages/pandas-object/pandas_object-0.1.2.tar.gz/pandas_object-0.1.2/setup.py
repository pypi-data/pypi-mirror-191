# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_object']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.0,<2.0.0', 'rich>=13.3.1,<14.0.0']

setup_kwargs = {
    'name': 'pandas-object',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'dwpeng',
    'author_email': '1732889554@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
