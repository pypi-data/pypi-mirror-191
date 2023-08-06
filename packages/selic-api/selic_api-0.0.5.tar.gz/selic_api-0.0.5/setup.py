# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selic_api']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'selic-api',
    'version': '0.0.5',
    'description': 'API para obtenção dos dados da SELIC.',
    'long_description': '# selic_api\n API para obter a taxa SELIC acumulada para fins de cálculo da atualização monetária para os tributos da Prefeitura de Belo Horizonte.\n',
    'author': 'João Marcelo',
    'author_email': 'joaomarceloav@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marceloid/selic_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
