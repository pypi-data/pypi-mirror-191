import enum
import typing
from typing import Any, Optional

from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE
from ms_graph_client.graph_api_config import GraphAPIConfig
from ms_graph_client.exceptions import NoMatchingGroupError, TooManyMatchingGroupsError
import datetime
import time


class Groups(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig):
        super().__init__(config=config)

    class GroupType(enum.Enum):
        SECURITY: str = "SECURITY"
        Microsoft365: str = "Microsoft365"

    def is_group_assigned_to_app(self, app_service_principal_id: str, group_id: str) -> bool:

        # Lame -
        # https://learn.microsoft.com/en-us/answers/questions/603125/how-to-filter-approleassignments-based-on-approlei
        # No searching or filtering.....

        # myresp = self._get(url_part="/servicePrincipals/" +
        #                             app_sp_id +
        #                             "/appRoleAssignments" + "?$filter=principalId eq '" + principal_id + "'")
        #                             #"/appRoleAssignedTo"+"?$filter=principalId eq '" + principal_id + "'" )
        #
        # results = myresp["value"]
        # if len(results) > 2 :
        #     raise Exception("Unexpected")
        #
        # if len(results) == 1:
        #     return True
        # else:
        #     return False

        # Hack workaround - go by group instead of app.
        # Each Group will be assigned to far fewer apps than total groups in APP

        # Far more efficient.
        # Could be slightly more efficient by checking each loop to see if its true - but good enough for now.
        # https://graph.microsoft.com/v1.0/groups/1a672c66-a0b9-4f08-af97-da14e6a3b93b/appRoleAssignments

        group_role_assignments = []
        json = self._get(url_part="/groups/" + group_id + "/appRoleAssignments")
        for assign in json["value"]:
            group_role_assignments.append(assign)

        js = json

        while "@odata.nextLink" in js:
            js = self._get(url_part=js["@odata.nextLink"])

            for temp_member in js["value"]:
                group_role_assignments.append(temp_member)

        for val in group_role_assignments:
            if val["resourceId"] == app_service_principal_id:
                return True

        return False

    def get_by_object_id(self, group_id: str) -> Any:
        res = self._get(url_part="/groups/" + group_id)
        return res

    def get_by_name(self, group_name: str) -> Any:
        res = self._get(url_part="/groups?$filter=displayName eq '" + group_name + "'")
        results = res["value"]
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            raise TooManyMatchingGroupsError("Group Name: " + group_name)
        else:
            raise NoMatchingGroupError("Group Name: " + group_name)

    def exists_by_name(self, group_name: str) -> bool:
        # Does Group already exist?
        # https://learn.microsoft.com/en-us/graph/api/group-list?view=graph-rest-1.0&tabs=http
        # GroupMember.Read.All,
        # Group.Read.All,
        # Directory.Read.All,
        # Group.ReadWrite.All,
        # Directory.ReadWrite.All

        try:
            self.get_by_name(group_name=group_name)
            return True
        except (NoMatchingGroupError):
            return False

    def delete(self, group_id: str, group_name: str, with_stabilization: bool) -> None:
        self._delete(url_part="/groups/" + group_id)

        if with_stabilization:
            self._stabilize_group_existence(group_name=group_name, should_exist=False)

    def update(self, group_id: str, group_name: Optional[str] = None, group_description: Optional[str] = None) -> None:
        data = {}

        if group_description is not None:
            data.update({"description": group_description})

        if group_name is not None:
            data.update({"displayName": group_name})

        self._patch(url_part="/groups/" + group_id, json=data)

    def list_owners(self, group_id: str) -> list[Any]:

        owners = []

        json = self._get(url_part="/groups/" + group_id + "/owners")

        for temp_owner in json["value"]:
            owners.append(temp_owner)

        js = json

        while "@odata.nextLink" in js:
            js = self._get(url_part=js["@odata.nextLink"])

            for temp_owner in js["value"]:
                owners.append(temp_owner)

        return owners

    def add_owner(self, group_id: str, user_obj_id: str) -> None:
        from ms_graph_client import Generator

        data = {"@odata.id": Generator(self.config).user_url(user_obj_id=user_obj_id)}
        self._post(url_part="/groups/" + group_id + "/owners/$ref", json=data)

    def remove_owner(self, group_id: str, user_obj_id: str) -> None:
        self._delete(url_part="/groups/" + group_id + "/owners/" + user_obj_id + "/$ref")

    def _stabilize_group_existence(self, group_name: str, should_exist: bool) -> None:
        expected_total_times = 4
        total_times_found = 0
        sleep_time = 3
        print(datetime.datetime.now().isoformat() + " - Stabilization Started")

        while True:
            if self.exists_by_name(group_name=group_name):
                if should_exist:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break
                else:
                    total_times_found = 0
            else:
                if should_exist:
                    total_times_found = 0
                else:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break

            time.sleep(sleep_time)

        time.sleep(3)
        print(datetime.datetime.now().isoformat() + " - Stabilization Succeeded")

    def create(
        self,
        group_name: str,
        group_description: str,
        group_type: GroupType,
        owners: list[str],
        with_stabilization: bool,
    ) -> str:
        # Does Group already exist?
        if self.exists_by_name(group_name=group_name):
            raise Exception("Group already exists")

        if group_type == Groups.GroupType.SECURITY:
            group_types = []
        elif group_type == Groups.GroupType.Microsoft365:
            group_types = ["Unified"]
        else:
            raise NotImplementedError()

        import uuid

        data = {
            "displayName": group_name,
            "description": group_description,
            "mailEnabled": False,
            "mailNickname": str(uuid.uuid4()),
            "securityEnabled": True,
            "groupTypes": group_types,
            "owners@odata.bind": owners,
        }

        group_resp = self._post("/groups", json=data)
        group_id = group_resp["id"]

        if with_stabilization:
            self._stabilize_group_existence(group_name=group_name, should_exist=True)

        return typing.cast(str, group_id)

    def list_group_members(self, group_id: str) -> list[Any]:

        # List members with pagination
        # "/groups/{id}/members"
        members = []

        json = self._get(url_part="/groups/" + group_id + "/members")

        for temp_member in json["value"]:
            members.append(temp_member)

        js = json

        while "@odata.nextLink" in js:
            js = self._get(url_part=js["@odata.nextLink"])

            for temp_member in js["value"]:
                members.append(temp_member)

        return members

    def is_member_of_group(self, group_id: str, object_id: str) -> bool:
        for val in self.list_group_members(group_id=group_id):
            if val["id"] == object_id:
                return True

        return False

    def _stabilize_member_in_group_existence(self, group_id: str, object_id: str, should_exist: bool) -> None:
        expected_total_times = 4
        total_times_found = 0
        sleep_time = 3
        print(datetime.datetime.now().isoformat() + " - Stabilization Started")

        while True:
            if self.is_member_of_group(group_id=group_id, object_id=object_id):
                if should_exist:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break
                else:
                    total_times_found = 0
            else:
                if should_exist:
                    total_times_found = 0
                else:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break

            time.sleep(sleep_time)

        time.sleep(3)
        print(datetime.datetime.now().isoformat() + " - Stabilization Succeeded")

    def add_member(self, group_id: str, object_id: str, with_stabilization: bool) -> None:

        data = {"@odata.id": self.config.api_url + "/directoryObjects/" + object_id}

        self._post(url_part="/groups/" + group_id + "/members/$ref", json=data)

        if with_stabilization:
            self._stabilize_member_in_group_existence(group_id=group_id, object_id=object_id, should_exist=True)

    def _chunk_list(self, my_list: list[Any], size: int) -> typing.Iterator[Any]:
        from itertools import islice

        it = iter(my_list)
        return iter(lambda: tuple(islice(it, size)), ())

    def add_members(self, group_id: str, object_ids: list[str]) -> None:

        myiterator = self._chunk_list(object_ids, 20)

        for arr in myiterator:
            mydataarray = []

            for item in arr:
                mydataarray.append(self.config.api_url + "/directoryObjects/" + item)

            data = {"members@odata.bind": mydataarray}

            self._patch(url_part="/groups/" + group_id, json=data)

    def remove_member(self, group_id: str, object_id: str, with_stabilization: bool) -> None:
        self._delete(url_part="/groups/" + group_id + "/members/" + object_id + "/$ref")

        if with_stabilization:
            self._stabilize_member_in_group_existence(group_id=group_id, object_id=object_id, should_exist=False)
