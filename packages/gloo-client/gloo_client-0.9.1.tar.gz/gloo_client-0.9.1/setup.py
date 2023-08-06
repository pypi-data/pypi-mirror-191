# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gloo_client',
 'gloo_client.model',
 'gloo_client.model.core',
 'gloo_client.model.resources',
 'gloo_client.model.resources.app',
 'gloo_client.model.resources.document',
 'gloo_client.model.resources.document_group',
 'gloo_client.model.resources.internal',
 'gloo_client.model.resources.util']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-requests>=2.28.11.1,<3.0.0.0']

setup_kwargs = {
    'name': 'gloo-client',
    'version': '0.9.1',
    'description': '',
    'long_description': 'This is a client to talk to gloo search API.\n',
    'author': 'Vaibhav Gupta',
    'author_email': 'vbv@gloo.chat',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
