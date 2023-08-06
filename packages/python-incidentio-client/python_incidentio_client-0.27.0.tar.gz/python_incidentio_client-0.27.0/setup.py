# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['incident_io_client',
 'incident_io_client.api',
 'incident_io_client.api.actions_v1',
 'incident_io_client.api.custom_field_options_v1',
 'incident_io_client.api.custom_fields_v1',
 'incident_io_client.api.incident_attachments_v1',
 'incident_io_client.api.incident_roles_v1',
 'incident_io_client.api.incident_statuses_v1',
 'incident_io_client.api.incident_timestamps_v2',
 'incident_io_client.api.incident_types_v1',
 'incident_io_client.api.incidents_v1',
 'incident_io_client.api.incidents_v2',
 'incident_io_client.api.severities_v1',
 'incident_io_client.api.utilities_v1',
 'incident_io_client.api.webhooks',
 'incident_io_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0', 'httpx>=0.22.0', 'python-dateutil>=2.8.0']

setup_kwargs = {
    'name': 'python-incidentio-client',
    'version': '0.27.0',
    'description': 'Python client for Incident.io',
    'long_description': '# python-incident-io-client\n\n![main build status](https://github.com/expobrain/python-incidentio-client/actions/workflows/main.yml/badge.svg?branch=main)\n\nA client library for accessing incident.io.\n\n## Installation\n\nTo install the client:\n\n```shell\npip install python-incidentio-client\n```\n\n## Usage\n\nFirst, create a client:\n\n```python\nfrom incident_io_client import Client\n\nclient = Client(base_url="https://api.incident.io")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom incident_io_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.incident.io", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom incident_io_client.models import MyDataModel\nfrom incident_io_client.api.my_tag import get_my_data_model\nfrom incident_io_client.types import Response\n\nmy_data: MyDataModel = get_my_data_model.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom incident_io_client.models import MyDataModel\nfrom incident_io_client.api.my_tag import get_my_data_model\nfrom incident_io_client.types import Response\n\nmy_data: MyDataModel = await get_my_data_model.asyncio(client=client)\nresponse: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)\n```\n\nBy default, when you\'re calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.incident.io",\n    token="SuperSecretToken",\n    verify_ssl="/path/to/certificate_bundle.pem",\n)\n```\n\nYou can also disable certificate validation altogether, but beware that **this is a security risk**.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.incident.io",\n    token="SuperSecretToken",\n    verify_ssl=False\n)\n```\n\nThings to know:\n\n1. Every path/method combo becomes a Python module with four functions:\n\n   1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n   1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n   1. `asyncio`: Like `sync` but the async instead of blocking\n   1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `incident_io_client.api.default`\n\n## Generate code\n\nThis client is automatically generated from the Swagger 2.x specs downloaded from the [openapi-python-client](https://pypi.org/project/openapi-python-client/)\'s [definition endpoint](https://api-docs.incident.io/#operation/Utilities_OpenAPI); a code generator tool will use the OpenAPI document to generates a sync/async client.\n\nTo generare an updated copy of the client:\n\n```shell\npoetry install\nmake download\npoetry run make generate\n```\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/expobrain/python-incidentio-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
