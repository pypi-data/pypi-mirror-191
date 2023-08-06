from typing import Any

from ms_graph_client.services.applications import Applications as ApplicationsCrud

import cachetools.func


class Applications:
    def __init__(self, crud_client: ApplicationsCrud):
        self._crud_client = crud_client

    @cachetools.func.ttl_cache(ttl=300)
    def get_by_application_name(self, app_name: str) -> Any:
        return self._crud_client.get_by_application_name(app_name=app_name)

    @cachetools.func.ttl_cache(ttl=300)
    def get_service_principal_by_app_id(self, app_id: str) -> Any:
        return self._crud_client.get_service_principal_by_app_id(app_id=app_id)

    @cachetools.func.ttl_cache(ttl=300)
    def exists_by_obj_id(self, id: str) -> bool:
        return self._crud_client.exists_by_obj_id(id=id)

    @cachetools.func.ttl_cache(ttl=300)
    def get_by_object_id(self, id: str) -> Any:
        return self._crud_client.get_by_object_id(id=id)
