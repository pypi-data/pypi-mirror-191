# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['planetmint_cryptoconditions',
 'planetmint_cryptoconditions.schemas',
 'planetmint_cryptoconditions.types']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl==1.4.0',
 'base58==2.1.1',
 'cryptography==39.0.1',
 'pyasn1==0.4.8',
 'setuptools>=67.2.0,<68.0.0',
 'zenroom>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'planetmint-cryptoconditions',
    'version': '1.1.2',
    'description': 'Multi-algorithm, multi-level, multi-signature format for expressing conditions and fulfillments according to the Interledger Protocol (ILP).',
    'long_description': ".. image:: https://badge.fury.io/py/planetmint-cryptoconditions.svg\n        :target: https://badge.fury.io/py/planetmint-cryptoconditions\n\n.. image:: https://app.travis-ci.com/planetmint/cryptoconditions.svg?branch=main\n        :target: https://app.travis-ci.com/planetmint/cryptoconditions\n\n.. image:: https://codecov.io/gh/planetmint/cryptoconditions/branch/main/graph/badge.svg?token=2Bo1knLW0Q\n        :target: https://codecov.io/gh/planetmint/cryptoconditions\n    \nThe cryptoconditions Package\n============================\n\nA Python implementation of the Crypto-Conditions spec: a multi-algorithm, multi-level, multi-signature format for expressing conditions and fulfillments.\n\nThis implementation doesn't implement the entire Crypto-Conditions spec. It implements the conditions needed by Planetmint, and some others. It's compliant with `version 02 <https://tools.ietf.org/html/draft-thomas-crypto-conditions-02>`_ and `version 04 <https://tools.ietf.org/html/draft-thomas-crypto-conditions-03>`_ of the spec.\n\n\nPlanetmint-Cryptoconditions (versions >= 1.0.0) extend previously designed cryptoconditions with Zencode based conditions and fulfillments.\nZencode is an extendable lua-based scripting and contracting language and is executed within the Zenroom virtual machine.\nZenroom and Zencode are developed by `Dyne <https://www.dyne.org/>`_. `Details <https://github.com/dyne/Zenroom>`_ and documenation exist at `Zenroom.org <https://zenroom.org/>`_.\n\n\nSee also: \n\n* the `rfcs/crypto-conditions repository <https://github.com/rfcs/crypto-conditions>`_\n \n* the `Zenroom documentation <https://github.com/dyne/Zenroom>`_\n\nPre-conditions\n--------------\n\nCryptoconditions require a Python version above 3.8.\n\nInstallation\n------------\n\nTo install latest release from PyPI:\n\n.. code-block:: bash\n\n    $ pip install planetmint-cryptoconditions\n\nDocumentation\n-------------\nPublic documentation is available at `https://docs.planetmint.io/projects/cryptoconditions/ <https://docs.planetmint.io/projects/cryptoconditions/en/latest/>`_.\n\n\nDevelopment\n-----------\nThis project uses `poetry <https://python-poetry.org/>` for dependency management.\nRun `poetry install` to start local development.\n",
    'author': 'Cryptoconditions contributors',
    'author_email': 'contact@ipdb.global',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/planetmint/cryptoconditions/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
