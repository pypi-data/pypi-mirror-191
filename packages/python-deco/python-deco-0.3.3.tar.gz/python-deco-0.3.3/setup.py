# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_deco', 'py_deco.dev', 'py_deco.dev.debug', 'py_deco.time']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'python-deco',
    'version': '0.3.3',
    'description': '',
    'long_description': '# py_decorators\n\nAn OSS that has something to do with decorators in python\n\n# credits\n\nhttps://bytepawn.com/python-decorators-for-data-scientists.html\n',
    'author': 'adrian',
    'author_email': 'tamkayeung.adrian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
