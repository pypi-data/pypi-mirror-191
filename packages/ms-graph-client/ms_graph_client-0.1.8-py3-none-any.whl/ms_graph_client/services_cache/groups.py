from typing import Any
import cachetools.func
from ms_graph_client.services.groups import Groups as GroupsCrud


class Groups:
    def __init__(self, crud_client: GroupsCrud):
        self._crud_client = crud_client

    @cachetools.func.ttl_cache(ttl=300)
    def is_group_assigned_to_app(self, app_service_principal_id: str, group_id: str) -> bool:
        return self._crud_client.is_group_assigned_to_app(
            app_service_principal_id=app_service_principal_id, group_id=group_id
        )

    @cachetools.func.ttl_cache(ttl=300)
    def get_by_name(self, group_name: str) -> Any:
        return self._crud_client.get_by_name(group_name=group_name)

    @cachetools.func.ttl_cache(ttl=300)
    def exists_by_name(self, group_name: str) -> bool:
        return self._crud_client.exists_by_name(group_name=group_name)

    @cachetools.func.ttl_cache(ttl=300)
    def list_group_members(self, group_id: str) -> list[Any]:
        return self._crud_client.list_group_members(group_id=group_id)

    @cachetools.func.ttl_cache(ttl=300)
    def is_member_of_group(self, group_id: str, object_id: str) -> bool:
        return self._crud_client.is_member_of_group(group_id=group_id, object_id=object_id)
