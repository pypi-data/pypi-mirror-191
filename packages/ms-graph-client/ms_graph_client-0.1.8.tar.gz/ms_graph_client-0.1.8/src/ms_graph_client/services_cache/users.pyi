from ms_graph_client.services.users import Users as UsersCrud
from typing import Any

class Users:
    _crud_client: UsersCrud
    def __init__(self, crud_client: UsersCrud) -> None: ...
    def get_user(self, upn: str) -> Any: ...
