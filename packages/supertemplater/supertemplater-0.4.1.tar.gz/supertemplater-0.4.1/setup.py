# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supertemplater',
 'supertemplater.builders',
 'supertemplater.models',
 'supertemplater.protocols']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.29,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['supertemplater = supertemplater.cli:main']}

setup_kwargs = {
    'name': 'supertemplater',
    'version': '0.4.1',
    'description': '',
    'long_description': '# SuperTemplater\n\n<!-->TODO<!-->\n',
    'author': 'Alexis Beaulieu',
    'author_email': 'alexisbeaulieu97@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexisbeaulieu97/SuperTemplater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
