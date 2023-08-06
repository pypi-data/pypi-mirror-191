# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virttop']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0', 'libvirt-python>=9.0.0,<10.0.0']

entry_points = \
{'console_scripts': ['virttop = virttop.virttop:main']}

setup_kwargs = {
    'name': 'virttop',
    'version': '0.1.1',
    'description': 'A top like utility for libvirt',
    'long_description': '# virttop\na top like utility for libvirt\n',
    'author': 'terminaldweller',
    'author_email': 'devi@terminaldweller.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/terminaldweller/virttop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
