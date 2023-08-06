from ms_graph_client.graph_api_config import GraphAPIConfig as GraphAPIConfig
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE as GraphAPICRUDBASE
from typing import Any

class Users(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig) -> None: ...
    def get_user(self, upn: str) -> Any: ...
