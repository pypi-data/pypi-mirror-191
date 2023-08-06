# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hc_pyconsul', 'hc_pyconsul.helpers', 'hc_pyconsul.lib', 'hc_pyconsul.models']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['httpx>=0.23.0,<0.24.0',
 'opentelemetry-api>=1.13.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'hc-pyconsul',
    'version': '0.3.1',
    'description': 'API client for HashiCorp Consul',
    'long_description': 'None',
    'author': 'Arden Shackelford',
    'author_email': 'arden@ardens.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
