# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['motor-stubs']

package_data = \
{'': ['*'], 'motor-stubs': ['aiohttp/*', 'frameworks/*']}

install_requires = \
['pymongo>=4.3.0', 'typing-extensions>=4.0.0']

extras_require = \
{'motor': ['motor>=3.0.0', 'dnspython>=2.3.0']}

setup_kwargs = {
    'name': 'motor-types',
    'version': '1.0.0b1',
    'description': "Python stubs for Motor, a Non-Blocking MongoDB driver for Python's Tornado and AsyncIO based applications.",
    'long_description': 'Motor-Types\n===========\nPython stubs for [Motor], a Non-Blocking [MongoDB] driver for [Python]\'s [Tornado] and [AsyncIO] based applications.\n\nAbout\n------\nStubs for [Motor] (version 3.0.0+) for substituting the missing type-hints. These stubs are meant to be used along with\npycharm and mypy to facilitate static type-checking. Installing this package adds these `.pyi` files to\n`libs/site-packages/motor`. Currently, only the stubs for [AsyncIO] are supported. You can contribute to stubs for\n[Tornado] by opening a pull request for the same.\n\n**Note:** This project is currently under development and is in no way affiliated with MongoDB. This is an unofficial\nstub package.\n\nHow to use?\n-----------\n\nYou can either install from [PyPI] using [pip] or add files to your project directories manually.\n\n### Installing Using [pip]:\n```commandline\npip install motor-types\n```\n\n### To install [Motor] (and [Dnspython]) alongside the package:\n```commandline\npip install motor-types[motor]\n```\n\n### To add files to the project manually:\nUse this command to clone the repository:\n```commandline\ngit clone "https://github.com/L0RD-ZER0/Motor-Types"\n```\n\nAfterwards, you can do either of the following to use stubs:\n* Copy the stubs manually to either ``libs/site-packages/motor`` or ``libs/site-packages/motor-stubs``, ideally the latter.\n* Add these stubs manually to project directories.\n  * [For MyPy][MyPy-Stubs].\n  * [For PyCharm][PyCharm-Stubs].\n  * For other static type-checking tools, consider referring to their corresponding documentation regarding stubs.\n\nExamples:\n---------\n### Auto-Complete Example\n**Without Stubs:**\n\n![ACNS]\n\n**With Stubs:**\n\n![ACWS]\n\n### Type-Checking Example\n**Without Stubs:**\n\n![TCNS]\n\n**With Stubs:**\n\n![TCWS]\n\nDependencies\n------------\nThis package uses following dependencies:\n* [Poetry] (For Packaging and Publishing)\n* [PyMongo] (For PyMongo related types)\n* [Motor] (For Referencing and for motor installation extra)\n* [Dnspython] (For motor installation extra)\n* [Pre-Commit] (For maintaining code quality)\n* [Typing-Extensions] (For using the latest typing features)\n\nHow to Contribute?\n------------------\nThe simplest contribution you can make is by opening a [GitHub Issue][GH-Issues] or by forking the repository and making\na pull request on the [GitHub Repository][GH-Repo] for the same. The changes can be as simple as improving the\ndocumentation or as big as completing any incomplete section of the typings.\n\n**Note:** All issues and pull-requests are subjected to a preliminary inspection.\n\nLicense\n-------\nThis repository is licensed under MIT License. The [license][License] can be found within the repository.\n\n\n[Motor]: https://github.com/mongodb/motor\n[MongoDB]: https://www.mongodb.com\n[PyMongo]: https://github.com/mongodb/mongo-python-driver\n[Poetry]: https://github.com/python-poetry/poetry\n[pip]: https://pypi.org/project/pip/\n[Dnspython]: https://www.dnspython.org/\n[Pre-Commit]: https://pre-commit.com\n[Typing-Extensions]: https://github.com/python/typing_extensions\n[Python]: https://python.org\n[Tornado]: https://www.tornadoweb.org/\n[Asyncio]: https://docs.python.org/3/library/asyncio.html\n[PyPI]: https://pypi.org/\n[MyPy-Stubs]: https://mypy.readthedocs.io/en/stable/stubs.html#stub-files\n[PyCharm-Stubs]: https://www.jetbrains.com/help/pycharm/stubs.html\n[GH-Repo]: https://github.com/L0RD-ZER0/Motor-Types\n[GH-Issues]: https://github.com/L0RD-ZER0/Motor-Types/issues\n[License]: https://github.com/L0RD-ZER0/Motor-Types/blob/master/LICENSE\n[ACNS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/auto-complete-example-ns.png\n[ACWS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/auto-complete-example-ws.png\n[TCNS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/type-checking-example-ns.png\n[TCWS]: https://github.com/L0RD-ZER0/Motor-Types/raw/master/examples/type-checking-example-ws.png',
    'author': 'L0RD-ZER0',
    'author_email': 'ackerhon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/L0RD-ZER0/Motor-Types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0',
}


setup(**setup_kwargs)
