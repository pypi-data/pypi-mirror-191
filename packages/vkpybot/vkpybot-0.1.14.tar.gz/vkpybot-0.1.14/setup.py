# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkpybot']

package_data = \
{'': ['*']}

install_requires = \
['aioboto3>=10.4.0,<11.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'docstring-parser>=0.15,<0.16',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'vkpybot',
    'version': '0.1.14',
    'description': 'Asyncronus library to build VK bot',
    'long_description': "VK is library that allows to create chatbots for vk easy and fast\n\n# Quickstart\n\nEasiest hi-bot\n\n    from VK import Bot\n\n\n    bot = Bot(api_token)\n\n    @bot.command('hi')\n    def greet(message):\n        return 'Hi'\n    \n    bot.start()\n",
    'author': 'Vlatterran',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Vlatterran/vkpybot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
