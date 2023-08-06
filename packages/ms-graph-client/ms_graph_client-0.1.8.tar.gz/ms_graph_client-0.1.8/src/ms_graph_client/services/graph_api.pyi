from .applications import Applications as Applications
from .groups import Groups as Groups
from .users import Users as Users
from ms_graph_client.graph_api_config import GraphAPIConfig as GraphAPIConfig

class GraphAPI:
    groups: Groups
    applications: Applications
    users: Users
    def __init__(self, config: GraphAPIConfig) -> None: ...
