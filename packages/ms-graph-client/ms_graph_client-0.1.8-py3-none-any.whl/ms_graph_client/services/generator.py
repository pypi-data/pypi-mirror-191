from ms_graph_client import GraphAPIConfig


class Generator:
    def __init__(self, config: GraphAPIConfig):
        self.config = config

    def user_url(self, user_obj_id: str) -> str:
        return self.config.api_url + "/users/" + user_obj_id

    def service_principal_url(self, app_service_principal_id: str) -> str:
        return self.config.api_url + "/servicePrincipals/" + app_service_principal_id
