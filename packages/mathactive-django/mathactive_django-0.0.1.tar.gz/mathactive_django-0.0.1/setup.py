# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mathactive_site', 'mathactive_web', 'mathactive_web.migrations']

package_data = \
{'': ['*'], 'mathactive_web': ['static/*', 'templates/*']}

install_requires = \
['django>=4.1,<5.0', 'mathactive>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'mathactive-django',
    'version': '0.0.1',
    'description': 'Web Application for conversational active learning activities for math students - a math learning chatbot.',
    'long_description': None,
    'author': 'hobs',
    'author_email': 'engineering@tangibleai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
