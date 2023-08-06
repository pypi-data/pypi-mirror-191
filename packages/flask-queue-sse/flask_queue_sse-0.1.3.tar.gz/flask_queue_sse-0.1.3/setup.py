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
    'version': '0.1.3',
    'description': "A simple implementation of Server-Sent Events for Flask that doesn't require Redis pub/sub.",
    'long_description': '<h5 align="center">\n    <img src="https://raw.githubusercontent.com/vsnthdev/flask-queue-sse/designs/header.png" alt="flask-queue-sse">\n</h5>\n<p align="center">\n    <strong>\n        A simple implementation of <a href="https://web.dev/eventsource-basics">Server-Sent Events</a> for <a\n            href="https://flask.palletsprojects.com">Flask</a> that\n        doesn\'t require Redis pub/sub.\n    </strong>\n</p>\n<p align="center">\n    <a target="_blank" rel="noopener" href="https://pypi.org/project/flask-queue-sse">\n        <img src="https://img.shields.io/pypi/v/flask-queue-sse?style=flat-square" alt="">\n    </a>\n    <a target="_blank" rel="noopener" href="https://pypi.org/project/flask-queue-sse/#history">\n        <img src="https://img.shields.io/pypi/dm/flask-queue-sse" alt="">\n    </a>\n    <a href="https://github.com/vsnthdev/flask-queue-sse/issues">\n        <img src="https://img.shields.io/github/issues/vsnthdev/flask-queue-sse.svg?style=flat-square" alt="">\n    </a>\n    <a href="https://github.com/vsnthdev/flask-queue-sse/commits/main">\n        <img src="https://img.shields.io/github/last-commit/vsnthdev/flask-queue-sse.svg?style=flat-square" alt="">\n    </a>\n</p>\n<br>\n\n<!-- header -->\n\n**flask-queue-sse** is my first ever Python library. It implements the Server-Sent Events protocol using the built-in Python `Queue` class. Please read [why this package](#💡-why-this-package) before using it in production.\n\n> Tweet to me <a target="_blank" rel="noopener" href="https://vas.cx/twitter">@vsnthdev</a>, I\'d love to know your\nexperience of this project 😀\n\n## 💡 Why this package\n\nMost implementations of Server-Sent Events available in PyPi for Flask require having a Redis database. This is to support horizontal scaling.\n\nThis library targets projects that don\'t want to deploy Redis seperately to get SSE working, and aren\'t aiming to horizontally scale _(have multiple instances of your app running behind a load balancer)_.\n\n## 💿 Installation\n\n```\npip install flask-queue-sse\n```\n\nPython 3.10 and above is required.\n\n## 🚀 Quick start\n\nAfter installing `flask-queue-sse`, you can start using it in the following way:\n\n```python\nfrom flask import Flask\nfrom flask_queue_sse import ServerSentEvents\n\napp = Flask(__name__)\n\n# storing sse events channel in memory\nsse: ServerSentEvents = None\n\n@app.route("/subscribe")\ndef subscribe():\n    # telling Python to refer to global sse variable\n    global sse\n\n    # create a new server sent events channel\n    sse = ServerSentEvents()\n\n    # create a new thread and do the actual work\n    # on it, pass sse instance to it for emitting events\n    \n    # when an "error" or "end" event is emitted\n    # the connection closes\n\n    # return it as a response\n    return sse.response()\n```\n\nLook into the [examples](https://github.com/vsnthdev/flask-queue-sse/tree/main/examples) or send me a message for any queries, questions or issues. I\'m always happy to help 😊\n\n## 💻 Building the project\n\n- 📁 Clone the repository.\n- 🏝️ Enter into the clonned directory & run `python -m venv .` to create a virtual environment.\n- 🔨 Install dependencies by running `pip install -r ./requirements.txt`.\n- 👨\u200d💻 Run the examples or edit the codebase.\n\n## 🏷️ Referrences\n\nThis library has been inspired by, and developed after consuming following resources:\n\n1. [Server-sent events in Flask without extra dependencies](https://maxhalford.github.io/blog/flask-sse-no-deps)\n2. [Why do I need redis?](https://github.com/singingwolfboy/flask-sse/issues/7)\n\n<!-- footer -->\n\n## 📰 License\n> The **flask-queue-sse** project is released under the [Zlib license](https://github.com/vsnthdev/flask-queue-sse/blob/main/LICENSE.md). <br> Developed &amp; maintained By Vasanth Srivatsa. Copyright 2023 © Vasanth Developer.\n<hr>\n\n> <a href="https://vsnth.dev" target="_blank" rel="noopener">vsnth.dev</a> &nbsp;&middot;&nbsp;\n> YouTube <a href="https://vas.cx/videos" target="_blank" rel="noopener">@VasanthDeveloper</a> &nbsp;&middot;&nbsp;\n> Twitter <a href="https://vas.cx/twitter" target="_blank" rel="noopener">@vsnthdev</a> &nbsp;&middot;&nbsp;\n> LinkedIn <a href="https://vas.cx/linkedin" target="_blank" rel="noopener">Vasanth Srivatsa</a>',
    'author': 'Vasanth Developer',
    'author_email': 'vsnthdev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
