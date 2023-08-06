# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks_vqe']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0,<4.0',
 'numpy==1.23.2',
 'qiskit>=0.41.0,<0.42.0',
 'strangeworks==0.4.0rc1',
 'tweedledum>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'strangeworks-vqe',
    'version': '0.1.0',
    'description': 'Extension to strangeworks sdk to allow user to run qaoa service',
    'long_description': '# strangeworks-vqe\n',
    'author': 'SFlann',
    'author_email': 'stuart@strangeworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
