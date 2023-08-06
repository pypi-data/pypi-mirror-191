# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ms_graph_client',
 'ms_graph_client.services',
 'ms_graph_client.services_cache']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.0.0,<6.0.0', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'ms-graph-client',
    'version': '0.1.8',
    'description': 'Provides a python wrapper around the Microsoft Graph API.  Current SDKs from Microsoft are in Preview mode.',
    'long_description': 'export PATH="$HOME/.local/bin:$PATH"\n\nDocs: https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0\n\n# How to use\n```\nfrom ms_graph_client import GraphAPI, GraphAPIConfig, GraphCacheAPI\nfrom ms_graph_client.services.groups import Groups\n\nclient_id = "xxxxxxxx"\ntenant_id = "xxxxxxxx"\nclient_secret = "xxxxxxxx"\n\ngraphapi_config = GraphAPIConfig(\n    client_id=client_id,\n    tenant_id=tenant_id,\n    client_secret=client_secret,\n    api_url="https://graph.microsoft.com/v1.0",\n)\n\n#CRUD wrapper to expose enough to automate Group Management.\n# This includes Create/Delete Azure AD Groups,\n# Add/Remove Members of Groups, \n# Assign and Unassign the group to/from an Application\n\ngraph_api_wrapper = GraphAPI(config=config)\n\n```',
    'author': 'Nick Carpenter',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/carpnick/ms_graph_client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
