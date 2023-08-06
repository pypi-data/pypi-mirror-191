# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['signhost', 'signhost.client', 'signhost.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'click>=8.0.1',
 'httpx>=0.23.3,<0.24.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyupgrade==3.3.1']

entry_points = \
{'console_scripts': ['signhost = signhost.__main__:main']}

setup_kwargs = {
    'name': 'signhost-api-python-client',
    'version': '0.1.4',
    'description': 'Signhost Api Python Client',
    'long_description': '# Signhost Api Python Client\n\n[![PyPI](https://img.shields.io/pypi/v/signhost-api-python-client.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/signhost-api-python-client.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/signhost-api-python-client)][python version]\n[![License](https://img.shields.io/pypi/l/signhost-api-python-client)][license]\n\n[![Read the documentation at https://signhost-api-python-client.readthedocs.io/](https://img.shields.io/readthedocs/signhost-api-python-client/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/foarsitter/signhost-api-python-client/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/foarsitter/signhost-api-python-client/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/signhost-api-python-client/\n[status]: https://pypi.org/project/signhost-api-python-client/\n[python version]: https://pypi.org/project/signhost-api-python-client\n[read the docs]: https://signhost-api-python-client.readthedocs.io/\n[tests]: https://github.com/foarsitter/signhost-api-python-client/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/foarsitter/signhost-api-python-client\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- 100% test coverage\n\n## Requirements\n\n- httpx\n- pydantic\n- attr\n- click\n\n## Installation\n\nYou can install _Signhost Api Python Client_ via [pip] from [PyPI]:\n\n```console\n$ pip install signhost-api-python-client\n```\n\n## Usage\n\n```python\nimport io\nfrom signhost import models\nfrom signhost.client import DefaultClient\n\nsignhost = DefaultClient(api_key="str", app_key="str")\ntransaction = models.Transaction(signers=[models.Signer(email="str")])\n\ntransaction = signhost.transaction_init(transaction=transaction)\nsignhost.transaction_file_put(\n    transaction.Id,\n    "file.pdf",\n    io.BytesIO(b"test"),\n)\ntransaction = signhost.transaction_start(transaction.Id)\n\nprint("Sign the contract over here", transaction.Signers[0].SignUrl)\n\nsignhost.transaction_get(transaction.Id)\nsignhost.transaction_file_get(transaction.Id, "file.pdf")\nsignhost.receipt_get(transaction.Id)\n```\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Signhost Api Python Client_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/foarsitter/signhost-api-python-client/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/foarsitter/signhost-api-python-client/blob/main/LICENSE\n[contributor guide]: https://github.com/foarsitter/signhost-api-python-client/blob/main/CONTRIBUTING.md\n[command-line reference]: https://signhost-api-python-client.readthedocs.io/en/latest/usage.html\n',
    'author': 'Jelmer Draaijer',
    'author_email': 'info@jelmert.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/foarsitter/signhost-api-python-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
