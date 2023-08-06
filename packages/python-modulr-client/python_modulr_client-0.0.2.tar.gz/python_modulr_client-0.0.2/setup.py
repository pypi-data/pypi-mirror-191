# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modulr_client',
 'modulr_client.api',
 'modulr_client.api.access_group',
 'modulr_client.api.accounts',
 'modulr_client.api.async_',
 'modulr_client.api.beneficiaries',
 'modulr_client.api.card_simulator',
 'modulr_client.api.cards',
 'modulr_client.api.confirmation_of_payee',
 'modulr_client.api.customers',
 'modulr_client.api.direct_debit_outbound',
 'modulr_client.api.direct_debits',
 'modulr_client.api.document',
 'modulr_client.api.file_upload',
 'modulr_client.api.inbound_payments',
 'modulr_client.api.notification',
 'modulr_client.api.payment_initiations',
 'modulr_client.api.payments',
 'modulr_client.api.restricted',
 'modulr_client.api.rules',
 'modulr_client.api.transactions',
 'modulr_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0', 'httpx>=0.22.0', 'python-dateutil>=2.8.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.4.0,<5.0.0']}

setup_kwargs = {
    'name': 'python-modulr-client',
    'version': '0.0.2',
    'description': 'Python client for Modulr APIs',
    'long_description': '# python-modulr-client\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/expobrain/python-modulr-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
