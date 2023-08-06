# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_f_richtext', 'wagtail_f_richtext.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['wagtail>=4.1,<5.0']

setup_kwargs = {
    'name': 'wagtail-f-richtext',
    'version': '1.0.0',
    'description': 'An alternative Wagtail richtext filter that applies classes or styles to rich text HTML content.',
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
