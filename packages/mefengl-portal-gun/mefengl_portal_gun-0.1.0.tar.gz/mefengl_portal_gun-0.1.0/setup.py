# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mefengl_portal_gun']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mefengl-portal-gun = mefengl_portal_gun.main:app']}

setup_kwargs = {
    'name': 'mefengl-portal-gun',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun\n',
    'author': '冯不游',
    'author_email': '71683364+mefengl@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
