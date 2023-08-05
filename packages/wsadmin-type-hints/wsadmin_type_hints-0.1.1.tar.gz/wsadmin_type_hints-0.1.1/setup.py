# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wsadmin_type_hints']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wsadmin-type-hints',
    'version': '0.1.1',
    'description': 'Provide type hints for `wsadmin` object methods',
    'long_description': "# `wsadmin-type-hints`\nPython package providing **type hints** for `wsadmin` **Jython** commands.\n\nThis speeds up the development of `wsadmin` **Jython** scripts inside an IDE since it provides intellisense on every method of the 5 main objects provided at runtime by the `wsadmin`:\n- `AdminControl`\n- `AdminConfig`\n- `AdminApp`\n- `AdminTask`\n- `Help`\n\n[📚 **Read the full documentation**](https://lukesavefrogs.github.io/wsadmin-type-hints/)\n\n# Disclaimer\nThis is an unofficial package created for speeding up the development process and is not in any way affiliated with IBM®. All trademarks and registered trademarks are the property of their respective company owners.\n\nThe code does not include any implementation detail, and includes only the informations (such as parameter numbers, types and descriptions) publicly available on the official Websphere Application Server® documentation.\n\n# Informations\n\nThis projects uses type hints, which were introduced in **Python 3.5**, so ensure you're using a supported version of python.\n\nFrom the [Python Stubs](https://typing.readthedocs.io/en/latest/source/stubs.html) documentation:\n> Type stubs are syntactically valid Python 3.7 files with a .pyi suffix. The Python syntax used for type stubs is independent from the Python versions supported by the implementation, and from the Python version the type checker runs under (if any). Therefore, type stub authors should use the latest available syntax features in stubs (up to Python 3.7), even if the implementation supports older, pre-3.7 Python versions.\n",
    'author': 'Luca Salvarani',
    'author_email': 'lucasalvarani99@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
