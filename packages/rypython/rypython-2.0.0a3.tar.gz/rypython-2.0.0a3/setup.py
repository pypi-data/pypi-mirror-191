# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rypython',
 'rypython.randas',
 'rypython.rex',
 'rypython.rexcel',
 'rypython.ry365',
 'rypython.ryagram',
 'rypython.rydb',
 'rypython.rysg',
 'rypython.ryteams',
 'rypython.rytime']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'O365>=2.0.18,<3.0.0',
 'PySimpleGUI>=4.60.3,<5.0.0',
 'PyYAML>=6.0,<7.0',
 'XlsxWriter>=3.0.2,<4.0.0',
 'html5lib>=1.1,<2.0',
 'lxml>=4.9.1,<5.0.0',
 'openpyxl>=3.0.9,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pymsteams>=0.2.1,<0.3.0',
 'pyodbc>=4.0.35,<5.0.0',
 'rich>=13.3.1,<14.0.0',
 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'rypython',
    'version': '2.0.0a3',
    'description': 'Miscellaneous python tools',
    'long_description': None,
    'author': "Ryan O'Rourke",
    'author_email': 'ryan@rypy.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
