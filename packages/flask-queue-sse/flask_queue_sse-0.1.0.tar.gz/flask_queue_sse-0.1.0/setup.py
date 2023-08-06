# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_queue_sse']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'flask-queue-sse',
    'version': '0.1.0',
    'description': "A simple implementation of Server-Sent Events for Flask that doesn't require Redis pub/sub.",
    'long_description': '## Flask Server Sent Events',
    'author': 'Vasanth Developer',
    'author_email': 'vsnthdev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
