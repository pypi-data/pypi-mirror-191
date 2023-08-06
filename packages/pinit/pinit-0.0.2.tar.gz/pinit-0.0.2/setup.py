# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinit', 'pinit..pinit']

package_data = \
{'': ['*'], 'pinit..pinit': ['ui/*', 'ui/assets/*']}

entry_points = \
{'console_scripts': ['pinit = pinit.main:main']}

setup_kwargs = {
    'name': 'pinit',
    'version': '0.0.2',
    'description': 'an application for creating shortcut for apps and scripts in linux',
    'long_description': '# pinit\n## an application for creating shortcut for apps and scripts ( only for linux )\n## installation\n- using pip :\nrun this two commands in terminal\n1. pip install pinit\n2. pinit\n- appimage :\njust download pinit.AppImage file and run it\n## commands\n- pinit\n- pinit install\n- pinit uninstall\n- pinit upgrade\n- pinit upgrade --force\n',
    'author': 'ramin',
    'author_email': 'ramin.kishani.farahani@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rraammiinn/pinit.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
