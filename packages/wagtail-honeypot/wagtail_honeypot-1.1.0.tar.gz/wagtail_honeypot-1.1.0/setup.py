# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_honeypot', 'wagtail_honeypot.templatetags']

package_data = \
{'': ['*'],
 'wagtail_honeypot': ['static/css/*', 'static/js/*', 'templates/tags/*']}

install_requires = \
['wagtail>=4.1']

setup_kwargs = {
    'name': 'wagtail-honeypot',
    'version': '1.1.0',
    'description': 'Use this package to add optional honeypot protection to your Wagtail forms.',
    'long_description': 'None',
    'author': 'Nick Moreton',
    'author_email': 'nickmoreton@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
