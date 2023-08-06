# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iolanta_jinja2']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'iolanta>=0.1.1,<0.2.0']

entry_points = \
{'iolanta.plugins': ['jinja2 = iolanta_jinja2:IolantaJinja2']}

setup_kwargs = {
    'name': 'iolanta-jinja2',
    'version': '0.1.0',
    'description': 'Render Jinja2 templates from Iolanta graph',
    'long_description': '# iolanta-jinja2\n\n\n',
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
