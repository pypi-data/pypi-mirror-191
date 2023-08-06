# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wibble']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fafa = wibble.wobble:wobble']}

setup_kwargs = {
    'name': 'wibble',
    'version': '0.0.1',
    'description': 'Minimal python project that exposes a commandline feature',
    'long_description': '# Wibble - a template for simple python packages\n\nA minimalist template for a python package.\n\nProvides the bl and the blarg commands.\n',
    'author': 'Joe Schmoe',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/retospect/wibble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
