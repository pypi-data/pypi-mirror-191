# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['novu', 'novu.api', 'novu.dto', 'novu.enums']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'sentry-sdk>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'novu',
    'version': '1.0.0a5',
    'description': 'This project aims to provide a wrapper for the Novu API.',
    'long_description': '# Novu Client (Python)\n\n[![PyPI](https://img.shields.io/pypi/v/novu-python?color=blue)](https://pypi.org/project/novu-python/)\n![Tests Status](https://github.com/ryshu/novu-python/actions/workflows/.github/workflows/tests.yml/badge.svg)\n[![codecov](https://codecov.io/gh/ryshu/novu-python/branch/main/graph/badge.svg?token=RON7F8QTZX)](https://codecov.io/gh/ryshu/novu-python)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/novu-python)\n![PyPI - License](https://img.shields.io/pypi/l/novu-python)\n[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)\n\n---\n\nThis project aims to provide a python wrapper for the Novu API.\n\n## Install\n\nTo install this package\n\n```shell\n# Via pip\npip install novu\n\n# Via poetry\npoetry add novu\n```\n\n## Quick start\n\nThis package is a wrapper of all the resources offered by Novu, we will just start by triggering an event on Novu.\n\nTo do this, you will need to:\n\n1. Follow Novu\'s procedure on how to set up your first template and keep in mind the identifier to trigger the template: https://docs.novu.co/overview/quick-start#create-a-notification-template\n2. Retrieve your API key from the platform directly in the settings section: https://web.novu.co/settings\n3. Play the following script:\n\n```python\nfrom novu.api import EventApi\n\nevent_api = EventApi("https://api.novu.co/api/", "<NOVU_API_TOKEN>")\nevent_api.trigger(\n    name="<YOUR_TEMPLATE_NAME>",\n    recipients="<YOUR_SUBSCRIBER_ID>",\n    payload={},  # Your Novu payload goes here\n)\n```\n\nIf all is ok, this should have triggered a notification in Novu.\n\n## Development\n\n```bash\n# install deps\npoetry install\n\n# pre-commit\npoetry run pre-commit install --install-hook\npoetry run pre-commit install --install-hooks --hook-type commit-msg\n```\n',
    'author': 'oscar.marie-taillefer',
    'author_email': 'oscar.marie-taillefer@spikeelabs.fr',
    'maintainer': 'oscar.marie-taillefer',
    'maintainer_email': 'oscar.marie-taillefer@spikeelabs.fr',
    'url': 'https://github.com/ryshu/novu-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
