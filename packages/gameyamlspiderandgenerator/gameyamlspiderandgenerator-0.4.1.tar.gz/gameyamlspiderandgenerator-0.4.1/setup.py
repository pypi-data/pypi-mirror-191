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
['beautifulsoup4>=4.11.2,<5.0.0',
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
    'version': '0.4.1',
    'description': '',
    'long_description': '# Start\n\n```commandline\npip install gameyamlspiderandgenerator -i https://pypi.org/simple\npython3.10\n```\n\n```python\nfrom gameyamlspiderandgenerator import produce_yaml\nfrom gameyamlspiderandgenerator.util.config import config\nfrom gameyamlspiderandgenerator.util.plugin_manager import pkg\n\nconfig.load("/home/user/desktop/config.yaml")\npkg.__init__()\nprint(produce_yaml("https://store.steampowered.com/app/1470120/Atopes/"))\n```\nconfig.yaml:\n```yaml\nplugin:\n  - steam\n  - itchio\nhook:\n  - search\n# if you don\'t want to set proxy, please fill in {}\n# http: socks5://127.0.0.1:7891\n# https: socks5://127.0.0.1:7891\nproxy: { }\ngitToken: \'your token\'\napi:\n  google-play: a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90\n  apple: a714b00383f0662a61b2e382d55c685f17015617aa7048972da58a756fb75e90\n```',
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
