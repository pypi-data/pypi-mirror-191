from typing import Any

from ms_graph_client.exceptions import UnableToFindUserError
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE
from ms_graph_client.graph_api_config import GraphAPIConfig
import requests


class Users(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig):
        super().__init__(config=config)

    def get_user(self, upn: str) -> Any:
        "carpnick2@qkdw.onmicrosoft.com"
        try:
            res = self._get(url_part="/users/" + upn)
            return res
        except Exception as e:
            if e.__cause__.__class__ == requests.exceptions.HTTPError:
                if e.__cause__.response.status_code == 404:
                    raise UnableToFindUserError(upn) from e
            # Default reraise
            raise
