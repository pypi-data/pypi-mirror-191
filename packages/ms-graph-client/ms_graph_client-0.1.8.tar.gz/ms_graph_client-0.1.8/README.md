export PATH="$HOME/.local/bin:$PATH"

Docs: https://learn.microsoft.com/en-us/graph/api/resources/group?view=graph-rest-1.0

# How to use
```
from ms_graph_client import GraphAPI, GraphAPIConfig, GraphCacheAPI
from ms_graph_client.services.groups import Groups

client_id = "xxxxxxxx"
tenant_id = "xxxxxxxx"
client_secret = "xxxxxxxx"

graphapi_config = GraphAPIConfig(
    client_id=client_id,
    tenant_id=tenant_id,
    client_secret=client_secret,
    api_url="https://graph.microsoft.com/v1.0",
)

#CRUD wrapper to expose enough to automate Group Management.
# This includes Create/Delete Azure AD Groups,
# Add/Remove Members of Groups, 
# Assign and Unassign the group to/from an Application

graph_api_wrapper = GraphAPI(config=config)

```