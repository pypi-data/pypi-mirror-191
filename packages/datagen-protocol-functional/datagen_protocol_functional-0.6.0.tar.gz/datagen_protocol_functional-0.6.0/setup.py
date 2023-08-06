# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datagen_protocol',
 'datagen_protocol.functional',
 'datagen_protocol.schema',
 'datagen_protocol.schema.assets',
 'datagen_protocol.schema.environment',
 'datagen_protocol.schema.hic',
 'datagen_protocol.schema.humans']

package_data = \
{'': ['*'], 'datagen_protocol': ['resources/*']}

install_requires = \
['dynaconf>=3.1.11,<4.0.0', 'numpy>=1.24.1,<2.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'datagen-protocol-functional',
    'version': '0.6.0',
    'description': 'Datagen Protocol Core',
    'long_description': 'None',
    'author': 'ShayZ',
    'author_email': 'shay.zilberman@datagen.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
