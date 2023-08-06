# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gameyamlspiderandgenerator',
 'gameyamlspiderandgenerator.hook',
 'gameyamlspiderandgenerator.plugin',
 'gameyamlspiderandgenerator.util']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'langcodes>=3.3.0,<4.0.0',
 'language-data>=1.1,<2.0',
 'loguru>=0.6.0,<0.7.0',
 'pillow>=9.4.0,<10.0.0',
 'pygithub>=1.57,<2.0',
 'pysocks>=1.7.1,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'ruamel-base>=1.0.0,<2.0.0',
 'ruamel.yaml.string>=0.1.0,<0.2.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'urllib3>=1.26.14,<2.0.0']

setup_kwargs = {
    'name': 'gameyamlspiderandgenerator',
    'version': '0.4',
    'description': '',
    'long_description': '',
    'author': 'kaesinol',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
