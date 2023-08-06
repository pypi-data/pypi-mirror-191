from ms_graph_client.graph_api_config import GraphAPIConfig
from .groups import Groups
from .applications import Applications
from .users import Users

from ms_graph_client.services.groups import Groups as GroupCrud
from ms_graph_client.services.applications import Applications as ApplicationsCrud
from ms_graph_client.services.users import Users as UserCrud


class GraphAPI:
    def __init__(self, config: GraphAPIConfig):
        self.groups = Groups(crud_client=GroupCrud(config=config))
        self.applications = Applications(
            crud_client=ApplicationsCrud(config=config, group_obj=GroupCrud(config=config))
        )
        self.users = Users(crud_client=UserCrud(config=config))
