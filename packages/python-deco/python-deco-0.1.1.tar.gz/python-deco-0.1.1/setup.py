# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_deco', 'py_deco.time']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-deco',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'adrian',
    'author_email': 'tamkayeung.adrian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
