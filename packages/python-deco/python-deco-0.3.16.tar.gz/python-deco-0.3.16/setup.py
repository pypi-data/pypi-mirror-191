# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyDeco', 'pyDeco.cli', 'pyDeco.debug', 'pyDeco.debug.debug', 'pyDeco.time']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'python-deco',
    'version': '0.3.16',
    'description': '',
    'long_description': '<div align="center">\n\n<h1> <strong>py</strong>thon <strong>Deco</strong>ractor<br>\n<img src="https://img.shields.io/badge/made%20with-LOVE-red">\n<img src="https://img.shields.io/badge/license-MIT-blue">\n<a href=\'https://py-decorators.readthedocs.io/en/latest/?badge=latest\'>\n    <img src=\'https://readthedocs.org/projects/py-decorators/badge/?version=latest\' alt=\'Documentation Status\' />\n</a>\n</h1>\n</div>\n\nAn OSS that has something to do with decorators in python\n\n# Features\n\n- Time related decorators\n- Debugging decorators\n- Custom cli input decorators\n\n# Example\n\n@timeit\n\n```python\nfrom pyDeco.dev import inactive\nfrom pyDeco.time import timeit\n\n@timeit\ndef func():\n    # do something\n    return 1\n```\n\n```bash\n pyDeco  | INFO | Function func() took 2.0261 seconds.\n```\n\n@stacktrace\n\n```python\nfrom pyDeco.dev import stacktrace\n\n\ndef nested_func():\n    print("nested")\n\n\ndef func_b():\n    print("func_b")\n    nested_func()\n\n\n@stacktrace\ndef func_a():\n    print("func_a")\n    func_b()\n    return 1\n\n\nfunc_a()\n```\n\n```terminal\n pyDeco  | INFO | @stacktrace set up for func_a()...\nfunc_a\n pyDeco  | INFO |       Executing func_b, line 9, from /mnt/Personal/test.py\nfunc_b\n pyDeco  | INFO |       Executing nested_func, line 5, from /mnt/Personal/test.py\nnested\n```\n\n##\n\n# TODO\n\n## credits\n\nhttps://bytepawn.com/python-decorators-for-data-scientists.html\n',
    'author': 'adrian',
    'author_email': 'tamkayeung.adrian@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://py-decorators.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
