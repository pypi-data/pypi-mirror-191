# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketbase',
 'pocketbase.models',
 'pocketbase.models.utils',
 'pocketbase.services',
 'pocketbase.services.utils',
 'pocketbase.stores']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'pocketbase',
    'version': '0.8.0',
    'description': 'PocketBase SDK for python.',
    'long_description': '# PocketBase Python SDK\n\n[![Tests](https://github.com/vaphes/pocketbase/actions/workflows/tests.yml/badge.svg)](https://github.com/vaphes/pocketbase/actions/workflows/tests.yml)\n\nPython client SDK for the <a href="https://pocketbase.io/">PocketBase</a> backend.\n\nThis is in early development, and at first is just a translation of <a href="https://github.com/pocketbase/js-sdk">the javascript lib</a> using <a href="https://github.com/encode/httpx/">HTTPX</a>.\n\n---\n\n## Installation\n\nInstall PocketBase using PIP:\n\n```shell\npython3 -m pip install pocketbase\n```\n\n## Usage\n\nThe rule of thumb here is just to use it as you would <a href="https://github.com/pocketbase/js-sdk">the javascript lib</a>, but in a pythonic way of course!\n\n```python\nfrom pocketbase import PocketBase  # Client also works the same\nfrom pocketbase.client import FileUpload\n\nclient = PocketBase(\'http://127.0.0.1:8090\')\n\n# authenticate as regular user\nuser_data = client.collection("users").auth_with_password(\n    "user@example.com", "0123456789")\n\n# or as admin\nadmin_data = client.admins.auth_with_password("test@example.com", "0123456789")\n\n# list and filter "example" collection records\nresult = client.collection("example").get_list(\n    1, 20, {"filter": \'status = true && created > "2022-08-01 10:00:00"\'})\n\n# create record and upload file to image field\nresult = client.collection("example").create(\n    {\n        "status": "true",\n        "image": FileUpload(("image.png", open("image.png", "rb"))),\n    })\n\n# and much more...\n```\n> More detailed API docs and copy-paste examples could be found in the [API documentation for each service](https://pocketbase.io/docs/api-authentication). Just remember to \'pythonize it\' 🙃.\n\n## Development\n\nThese are the requirements for local development:\n\n* Python 3.7+\n* Poetry (https://python-poetry.org/)\n\nYou can install locally:\n\n```shell\npoetry install\n```\n\nOr can build and generate a package:\n\n```shell\npoetry build\n```\n\nBut if you are using only PIP, use this command:\n\n```shell\npython3 -m pip install -e .\n```\n\n## Tests\n\nTo execute the tests use this command:\n\n```\npoetry run pytest\n```\n\n## License\n\nThe PocketBase Python SDK is <a href="https://github.com/vaphes/pocketbase/blob/master/LICENCE.txt">MIT licensed</a> code.\n',
    'author': 'Vithor Jaeger',
    'author_email': 'vaphes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vaphes/pocketbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
