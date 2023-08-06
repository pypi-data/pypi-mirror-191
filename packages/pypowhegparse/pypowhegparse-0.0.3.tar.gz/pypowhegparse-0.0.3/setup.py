# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypowhegparse']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'pandas', 'pytopdrawer', 'scipy', 'smpl', 'uncertainties']

entry_points = \
{'console_scripts': ['pypowhegparse = pypowhegparse.pypowhegparse:main']}

setup_kwargs = {
    'name': 'pypowhegparse',
    'version': '0.0.3',
    'description': 'Analyse POWHEG output files for potential errors.',
    'long_description': '# pypowhegparse\n\nAnalyse POWHEG output files for potential errors.',
    'author': 'Alexander Puck Neuwirth',
    'author_email': 'alexander@neuwirth-informatik.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/APN-Pucky/pypowhegparse.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
