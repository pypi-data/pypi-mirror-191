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
    'version': '0.1.2',
    'description': "A simple implementation of Server-Sent Events for Flask that doesn't require Redis pub/sub.",
    'long_description': '<h1 align="center">\n    <pre>flask-queue-sse</pre>\n</h1>\n<p align="center">\n    <strong>\n        A simple implementation of <a href="https://web.dev/eventsource-basics">Server-Sent Events</a> for <a\n            href="https://flask.palletsprojects.com">Flask</a> that\n        doesn\'t require Redis pub/sub.\n    </strong>\n</p>\n<p align="center">\n    <a target="_blank" rel="noopener" href="https://pypi.org/project/flask-queue-sse">\n        <img src="https://img.shields.io/pypi/v/flask-queue-sse?style=flat-square" alt="">\n    </a>\n    <a target="_blank" rel="noopener" href="https://pypi.org/project/flask-queue-sse/#history">\n        <img src="https://img.shields.io/pypi/dm/flask-queue-sse" alt="">\n    </a>\n    <a href="https://github.com/vsnthdev/flask_queue_sse/issues">\n        <img src="https://img.shields.io/github/issues/vsnthdev/flask_queue_sse.svg?style=flat-square" alt="">\n    </a>\n    <a href="https://github.com/vsnthdev/flask_queue_sse/commits/main">\n        <img src="https://img.shields.io/github/last-commit/vsnthdev/flask_queue_sse.svg?style=flat-square" alt="">\n    </a>\n</p>\n<br>\n\n<!-- header -->\n\n> Tweet me <a target="_blank" rel="noopener" href="https://vas.cx/twitter">@vsnthdev</a>, I would love to know your\nopinion/experience on this project 😍\n\n<!-- why this package? -->\n\n## 💿 Installation\n\n```\npip install flask-queue-sse\n```\n\n<!-- quick start -->\n\n<!-- docs to build the project -->\n\n<!-- footer -->\n\n## 📰 License\n> The **flask-queue-sse** project is released under the [Zlib license](https://github.com/vsnthdev/flask-queue-sse/blob/main/LICENSE.md). <br> Developed &amp; maintained By Vasanth Srivatsa. Copyright 2023 © Vasanth Developer.\n<hr>\n\n> <a href="https://vsnth.dev" target="_blank" rel="noopener">vsnth.dev</a> &nbsp;&middot;&nbsp;\n> YouTube <a href="https://vas.cx/videos" target="_blank" rel="noopener">@vasanthdeveloper</a> &nbsp;&middot;&nbsp;\n> Twitter <a href="https://vas.cx/twitter" target="_blank" rel="noopener">@vsnthdev</a> &nbsp;&middot;&nbsp;\n> Discord <a href="https://vas.cx/discord" target="_blank" rel="noopener">Vasanth Developer</a>',
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
