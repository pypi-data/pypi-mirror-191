# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkpybot']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'docstring-parser>=0.15,<0.16',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'vkpybot',
    'version': '0.2.0',
    'description': 'Asyncronus library to build VK bot',
    'long_description': "VK is library that allows to create chatbots for vk easy and fast\n\n![PyPI](https://github.com/Vlatterran/vkpybot/actions/workflows/publish.yaml/badge.svg)\n![docs](https://github.com/Vlatterran/vkpybot/actions/workflows/docs-publish.yaml/badge.svg)\n![docs](https://github.com/Vlatterran/vkpybot/actions/workflows/test.yaml/badge.svg)\n![version](https://img.shields.io/pypi/v/vkpybot.svg)\n![py_version](https://img.shields.io/pypi/pyversions/vkpybot.svg)\n\n# Quickstart\n\nEasiest hi-bot\n\n    from VK import Bot\n\n\n    bot = Bot(api_token)\n\n    @bot.command('hi')\n    def greet(message):\n        return 'Hi'\n    \n    bot.start()\n",
    'author': 'Vlatterran',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Vlatterran/vkpybot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
