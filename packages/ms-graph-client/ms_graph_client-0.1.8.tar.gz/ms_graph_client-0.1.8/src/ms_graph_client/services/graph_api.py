from ms_graph_client.graph_api_config import GraphAPIConfig
from .groups import Groups
from .applications import Applications
from .users import Users


class GraphAPI:
    def __init__(self, config: GraphAPIConfig):
        self.groups = Groups(config=config)
        self.applications = Applications(config=config, group_obj=self.groups)
        self.users = Users(config=config)
