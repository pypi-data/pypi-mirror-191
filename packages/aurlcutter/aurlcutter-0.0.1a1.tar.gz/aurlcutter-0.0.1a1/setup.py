# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurlcutter', 'aurlcutter.cutters']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'aurlcutter',
    'version': '0.0.1a1',
    'description': 'Asynchronous lib for making short urls',
    'long_description': '<h1>aurlcutter</h1>\n\n#### Simple asynchronous python url shortener api wrapper\n\n---\n**Source code**: <a href="https://github.com/mesiriak/aurlcutter" target="_blank">https://github.com/mesiriak/aurlcutter</a>\n\n---\n\n\n### Installation guide:\n```\npip install aurlcutter\n```\n\n### For watcing full list of services:\n#\n```python\nfrom aurlcutter import Cutter\n\ncutter_instance = Cutter()\n\nprint(cutter_instance.cutters)\n\n>>> ["tinyurl", "isgd", "dagd", ...]\n```\n\n### Usage example:\n#\n```python\nfrom aurlcutter import Cutter\n\ncutter_instance = Cutter()\n\nyour_link = "www.google.com"\n\n# you can choose api what you need by yourself\ncutted_link = cutter_instance.tinyurl.cut(your_link)\n```\n',
    'author': 'Mesiriak',
    'author_email': 'iamzhv@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mesiriak/aurlcutter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
