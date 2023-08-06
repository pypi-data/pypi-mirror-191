# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kbcstorage',
 'kbcstorage.tests',
 'kbcstorage.tests.functional',
 'kbcstorage.tests.mocks']

package_data = \
{'': ['*']}

install_requires = \
['azure-storage-blob>=12.14.1,<13.0.0',
 'boto3>=1.26.69,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'kbcstorage',
    'version': '0.0.1',
    'description': 'Keboola Storage API',
    'long_description': "[![Build Status](https://travis-ci.org/keboola/sapi-python-client.svg?branch=master)](https://travis-ci.org/keboola/sapi-python-client)\n\n# Python client for the Keboola Storage API\nClient for using [Keboola Connection Storage API](http://docs.keboola.apiary.io/). This API client provides client methods to get data from KBC and store data in KBC. The endpoints \nfor working with buckets, tables and workspaces are covered.\n\n## Install\n\n`$ pip3 install git+https://github.com/keboola/sapi-python-client.git`\n\nor \n\n```bash\n$ git clone https://github.com/keboola/sapi-python-client.git && cd sapi-python-client\n$ python setup.py install\n```\n\n## Client Class Usage\n```\nfrom kbcstorage.client import Client\n\nclient = Client('https://connection.keboola.com', 'your-token')\n\n# get table data into local file\nclient.tables.export_to_file(table_id='in.c-demo.some-table', path_name='/data/')\n\n# save data\nclient.tables.create(name='some-table-2', bucket_id='in.c-demo', file_path='/data/some-table')\n\n# list buckets\nclient.buckets.list()\n\n# list bucket tables\nclient.buckets.list_tables('in.c-demo')\n\n# get table info\nclient.tables.detail('in.c-demo.some-table')\n\n```\n\n## Endpoint Classes Usage \n```\nfrom kbcstorage.tables import Tables\nfrom kbcstorage.buckets import Buckets\n\ntables = Tables('https://connection.keboola.com', 'your-token')\n\n# get table data into local file\ntables.export_to_file(table_id='in.c-demo.some-table', path_name='/data/')\n\n# save data\ntables.create(name='some-table-2', bucket_id='in.c-demo', file_path='/data/some-table')\n\n# list buckets\nbuckets = Buckets('https://connection.keboola.com', 'your-token')\nbuckets.list()\n\n# list bucket tables\nbuckets.list_tables('in.c-demo')\n\n# get table info\ntables.detail('in.c-demo.some-table')\n\n```\n\n## Docker image\nDocker image with pre-installed library is also available, run it via:\n\n```\ndocker run -i -t quay.io/keboola/sapi-python-client\n```\n\n## Tests\n\n```bash\n$ git clone https://github.com/keboola/sapi-python-client.git && cd sapi-python-client\n$ python setup.py test\n```\n\nor \n\n```bash\n$ docker-compose run --rm -e KBC_TEST_TOKEN -e KBC_TEST_API_URL sapi-python-client -m unittest discover\n```\n\n## Contribution Guide\nThe client is far from supporting the entire API, all contributions are very welcome. New API endpoints should \nbe implemeneted in their own class extending `Endpoint`. Naming conventions should follow existing naming conventions\nor those of the [API](http://docs.keboola.apiary.io/#). If the method contains some processing of the request or response, consult the corresponing [PHP implementation](https://github.com/keboola/storage-api-php-client) for reference. New code should be covered by tests.\n\nNote that if you submit a PR from your own forked repository, the automated functional tests will fail. This is limitation of [Travis](https://docs.travis-ci.com/user/pull-requests/#Pull-Requests-and-Security-Restrictions). Either run the tests locally (set `KBC_TEST_TOKEN` (your token to test project) and `KBC_TEST_API_URL` (https://connection.keboola.com) variables) or ask for access. In case, you need a project for local testing, feel free to [ask for one](https://developers.keboola.com/#development-project).\n\nThe recommended workflow for making a pull request is:\n\n```bash\ngit clone https://github.com/keboola/sapi-python-client.git\ngit checkout master\ngit pull\ngit checkout -b my-new-feature\n# work on branch my-new-feature\ngit push origin my-new-feature:my-new-feature\n```\n\nThis will create a new branch which can be used to make a pull request for your new feature.\n\n## License\n\nMIT licensed, see [LICENSE](./LICENSE) file.\n",
    'author': 'Lukas Langr',
    'author_email': 'lukas.langr@datasentics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
