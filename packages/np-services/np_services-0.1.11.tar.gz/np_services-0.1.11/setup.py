# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_services']

package_data = \
{'': ['*']}

install_requires = \
['backoff',
 'fabric>=2.7,<3.0',
 'np_session>=0.2',
 'pydantic>=1.10,<2.0',
 'pyzmq',
 'requests>=2,<3']

setup_kwargs = {
    'name': 'np-services',
    'version': '0.1.11',
    'description': 'Tools for interfacing with devices and services used in Mindscope Neuropixels experiments at the Allen Institute.',
    'long_description': '# service usage\n![Services](./services.drawio.svg)',
    'author': 'bjhardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
