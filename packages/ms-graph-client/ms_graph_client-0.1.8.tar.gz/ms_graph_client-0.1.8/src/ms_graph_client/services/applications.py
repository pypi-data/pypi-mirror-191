from typing import Any
from ms_graph_client.graph_api_crud_base import GraphAPICRUDBASE
from ms_graph_client.graph_api_config import GraphAPIConfig
from ms_graph_client.exceptions import UnableToFindApplicationError
from .groups import Groups
import datetime
import time


class Applications(GraphAPICRUDBASE):
    def __init__(self, config: GraphAPIConfig, group_obj: Groups):
        super().__init__(config=config)
        self._group_crud = group_obj

    def get_by_application_name(self, app_name: str) -> Any:
        app_find = self._get(url_part="/applications?" + "$filter=displayName eq '" + app_name + "'")
        total_length = len(app_find["value"])
        assert total_length == 1

        return app_find["value"][0]

    def get_service_principal_by_app_id(self, app_id: str) -> Any:
        sp_resp = self._get(url_part="/servicePrincipals(appId='" + app_id + "')")
        return sp_resp

    def exists_by_obj_id(self, id: str) -> bool:
        try:
            self.get_by_object_id(id)
            return True
        except UnableToFindApplicationError:
            return False

    def get_by_object_id(self, id: str) -> Any:
        # https://learn.microsoft.com/en-us/graph/api/application-get?view=graph-rest-1.0&tabs=http
        # Application.Read.All,
        # Application.ReadWrite.OwnedBy,
        # Application.ReadWrite.All

        res = self._get(url_part="/applications/" + id)
        return res

    def list_assignments_to_app(self, app_sp_id: str) -> list[Any]:
        assignments = []

        myresp = self._get(url_part="/servicePrincipals/" + app_sp_id + "/appRoleAssignedTo/")
        for val in myresp["value"]:
            assignments.append(val)

        js = myresp
        while "@odata.nextLink" in js:
            js = self._get(url_part=js["@odata.nextLink"])
            for temp_member in js["value"]:
                assignments.append(temp_member)

        return assignments

    def _stabilize_app_assignment(self, app_sp_id: str, group_id: str, should_be_assigned: bool) -> None:
        expected_total_times = 4
        total_times_found = 0
        sleep_time = 3

        print(datetime.datetime.now().isoformat() + " - Stabilization Started")
        while True:

            # Really inefficient way of doing it
            # Replacing with group data instead - group data will be far smaller than app searching.
            # for val in self.list_assignments_to_app(app_sp_id=app_sp_id):
            #     if val["principalId"] == principal_id:
            #         return True
            #
            # return False

            if self._group_crud.is_group_assigned_to_app(app_service_principal_id=app_sp_id, group_id=group_id):
                if should_be_assigned:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break
                else:
                    total_times_found = 0
            else:
                if should_be_assigned:
                    total_times_found = 0
                else:
                    total_times_found += 1
                    if total_times_found >= expected_total_times:
                        break

            time.sleep(sleep_time)

        time.sleep(3)
        print(datetime.datetime.now().isoformat() + " - Stabilization Succeeded")

    def assign_group_to_app(self, app_name: str, group_id: str, with_stabilization: bool, appRole: str = "User") -> Any:

        # FIND THE APPLICATION we are going to assign to
        aws_app_json = self.get_by_application_name(app_name=app_name)

        # Get service principal of app
        aws_sp_json = self.get_service_principal_by_app_id(aws_app_json["appId"])
        aws_sp_id = aws_sp_json["id"]

        if self._group_crud.is_group_assigned_to_app(app_service_principal_id=aws_sp_id, group_id=group_id):
            raise Exception("GroupId:" + group_id + " is already assigned to application app name: " + app_name)

        # Get the right app Role to assign the group to - appRole Role
        aws_app_role_id = None
        for role in aws_sp_json["appRoles"]:
            if role["displayName"] == appRole:
                aws_app_role_id = role["id"]

        assert aws_app_role_id is not None

        # Do the assignment
        data = {"principalId": group_id, "resourceId": aws_sp_id, "appRoleId": aws_app_role_id}
        myresp = self._post(url_part="/servicePrincipals/" + aws_sp_id + "/appRoleAssignedTo", json=data)

        if with_stabilization:
            self._stabilize_app_assignment(app_sp_id=aws_sp_id, group_id=group_id, should_be_assigned=True)

        return myresp

    def unassign_group_to_app(
        self, app_name: str, assigned_to_id: str, group_id: str, with_stabilization: bool
    ) -> None:

        # FIND THE APPLICATION we are going to assign to
        aws_app_json = self.get_by_application_name(app_name=app_name)

        # Get service prinicpal of app
        aws_sp_json = self.get_service_principal_by_app_id(aws_app_json["appId"])
        aws_sp_id = aws_sp_json["id"]

        self._delete(url_part="/servicePrincipals/" + aws_sp_id + "/appRoleAssignedTo/" + assigned_to_id)

        if with_stabilization:
            self._stabilize_app_assignment(app_sp_id=aws_sp_id, group_id=group_id, should_be_assigned=False)
