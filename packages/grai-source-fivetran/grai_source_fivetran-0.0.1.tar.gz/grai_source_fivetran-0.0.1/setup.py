# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_source_fivetran', 'grai_source_fivetran.fivetran_api']

package_data = \
{'': ['*']}

install_requires = \
['fivetran>=0.7.0,<0.8.0',
 'grai-client>=0.2.0,<0.3.0',
 'grai-schemas>=0.1.10,<0.2.0',
 'multimethod>=1.8,<2.0',
 'pydantic>=1.9.1,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'grai-source-fivetran',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Ian Eaves',
    'author_email': 'ian@grai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.13,<4.0.0',
}


setup(**setup_kwargs)
