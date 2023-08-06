# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['project47a', 'project47a.data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'project47a',
    'version': '0.1.0',
    'description': 'Code name generator',
    'long_description': '## Project 47A -- Code Name Generator\n\n````python\nfrom project47a import get_generator\n\ngen = get_generator("de")\nprint(gen())\n# krude Lichtwolke\nprint(gen())\n# schaler Wintertag\n````\n',
    'author': 'Henryk Plötz',
    'author_email': 'henryk@ploetzli.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
