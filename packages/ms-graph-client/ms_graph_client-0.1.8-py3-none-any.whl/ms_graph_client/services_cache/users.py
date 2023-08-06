from typing import Any

from ms_graph_client.services.users import Users as UsersCrud
import cachetools.func


class Users:
    def __init__(self, crud_client: UsersCrud):
        self._crud_client = crud_client

    @cachetools.func.ttl_cache(ttl=600)
    def get_user(self, upn: str) -> Any:
        res = self._crud_client.get_user(upn=upn)
        return res
