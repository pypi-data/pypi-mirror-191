# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twilio_async', 'twilio_async.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3', 'pydantic>=1.10.4']

setup_kwargs = {
    'name': 'twilio-python-async',
    'version': '0.2.0',
    'description': 'An asynchronous Twilio client',
    'long_description': '# Asynchronous Twilio Client\n\n[![Tests Status](https://github.com/sanders41/twilio-python-async/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/twilio-python-async/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/twilio-python-async/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/twilio-python-async/main)\n[![Coverage](https://codecov.io/github/sanders41/twilio-python-async/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/twilio-python-async)\n[![PyPI version](https://badge.fury.io/py/twilio-python-async.svg)](https://badge.fury.io/py/twilio-python-async)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twilio-python-async?color=5cc141)](https://github.com/sanders41/twilio-python-async)\n\nAn asynchronous [Twilio](https://www.twilio.com/) client\n\n## Installation\n\nUsing a virtual environment is recommended for installing this package. Once the virtual environment is created and activated install the package with:\n\n```sh\npip install meilisearch-python-async\n```\n\n## Useage\n\nWhen creating a client the twilio account sid and token can either be read from a `TWILIO_ACCOUNT_SID`\nand `TWILIO_AUTH_TOKEN` variables, or passed into the client at creation. Using environment variables\nis recommended. Examples below will assume the use of environment variables.\n\n### Send an SMS message\n\nMessages can be sent by either using a Twilio messaging service sid, or by passing a `from_` phone\nnumber. The messaging service sid can be read from a `TWILIO_MESSAGING_SERVICE_SID` environment\nvariable. The examples below assumes the use of the environment variable.\n\n```py\nfrom twilio_async import AsyncClient\n\n\nasync with AsyncClient() as client:\n    await client.message_create("My message", "+12068675309")\n```\n\n### Retrieve message logs\n\n```py\nfrom twilio_async import AsyncClient\n\n\nasync with AsyncClient() as client:\n    response = await client.get_message_logs()\n```\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sanders41/twilio-python-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
