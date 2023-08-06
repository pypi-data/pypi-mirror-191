import json
import requests
from http import HTTPStatus
from apiClientBase import BaseAPIClient


class NovumBatteriesClient(BaseAPIClient):
    # ********************************************************
    # Section for the Service Center info
    # ********************************************************

    def ping(self) -> dict:
        response = self._get_json("/api/batman/v1/")
        return response

    def get_info(self) -> dict:
        response = self._get_json("/api/batman/v1/info")
        return response

    def get_version(self) -> dict:
        response = self._get_json("/api/batman/v1/version")
        return response

    # ********************************************************
    # Section for the users
    # ********************************************************

    def login(self, email: str, password: str, storeUser=True) -> dict:
        header = {"authorization": "auth", "content-type": "application/json"}
        payload = {"username": email, "password": password}
        response = requests.post(self.host + "/api/batman/v1/login", data=json.dumps(payload), headers=header)
        if response.status_code != HTTPStatus.OK and storeUser == True:
            print("%s (%s)", response.text, response.status_code)
            return dict(profile=dict(email=None), jwt=None, user_id=None, token=None, jwt_auth_header=None)
        user = response.json()
        self.user = user
        return user

    def logout(self) -> str:
        response = self._get_json("/api/batman/v1/logout")
        return response["message"]

    def check_current_user_still_authenticated(self) -> dict:
        response = self._get_json("/api/batman/v1/check_token")
        return response

    # ********************************************************
    # Section for the Battery Types
    # ********************************************************

    def get_battery_types(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/batteryTypes", filter=filter, option=option, timeout=timeout)
        return response

    def get_battery_types_count(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/batteryTypes/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_battery_types_by_id(self, battery_type_id: str, timeout: float = 4.0) -> dict:
        response = self._get_json(f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout)
        return response

    def remove_battery_types_by_id(self, battery_type_id: str, timeout: float = 4.0) -> dict:
        response = self._remove(f"/api/batman/v1/batteryTypes/{battery_type_id}", timeout=timeout)
        return response

    def create_batttery_type(
        self,
        battery_type,
        timeout: float = 4.0,
    ) -> dict:
        battery_dict = battery_type
        response = self._post_json("/api/batman/v1/batteryTypes", data=battery_dict, timeout=timeout)
        return response

    def update_battery_type_by_id(self, battery_type_id: str, battery_type_info, timeout: float = 4.0) -> dict:
        response = self._fetch(
            "put", f"/api/batman/v1/batteryTypes/{battery_type_id}", data=battery_type_info, timeout=timeout
        )
        return response

    # ********************************************************
    # Section for the Datasets
    # ********************************************************

    def dataset_exists_on_remote(self, dataset_id: str, timeout: float = 4.0) -> bool:
        response = self._get_json(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        try:
            len(response["measured"]["measurement_cycles"]) != 0
            return True
        except:
            return False

    def create_dataset(self, dataset, timeout: float = 4.0) -> dict:
        response = self._post_json("/api/batman/v1/datasets/", data=dataset, timeout=timeout)
        return response

    def post_dataset(self, dataset, timeout: float = 4.0) -> dict:
        response = self._post_json("/api/batman/v1/datasets/", data=dataset, timeout=timeout)
        return response

    def get_dataset_by_id(self, dataset_id: str, timeout: float = 4.0) -> dict:
        response = self._get_json(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    def get_datasets(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/datasets", filter=filter, option=option, timeout=timeout)
        return response

    def get_datasets_count(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/datasets/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_datasets_count_by_battery(self, battery, filter=None, option=None, timeout: float = 4.0) -> dict:
        filter_with_id = {"meta.battery._id": battery.id}
        filter_with_id.update(filter)
        response = self._fetch(
            "get", "/api/batman/v1/datasets/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def update_dataset_by_id(self, dataset_id: str, timeout: float = 4.0) -> dict:
        response = self._post_json(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    def remove_dataset_by_id(self, dataset_id: str, timeout: float = 4.0) -> dict:
        response = self._remove(f"/api/batman/v1/datasets/{dataset_id}", timeout=timeout)
        return response

    # ********************************************************
    # Section for the Battery
    # ********************************************************

    def create_battery(self, battery, timeout: float = 4.0) -> dict:
        response = self._post_json("/api/batman/v1/batteries", data=battery, timeout=timeout)
        return response

    def get_battery_by_id(self, battery_id: str, timeout: float = 4.0) -> dict:
        response = self._get_json(f"/api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return response

    def update_battery(self, battery, timeout: float = 4.0) -> dict:
        response = self._put_json(f"/api/batman/v1/batteries/{battery['id']}", timeout=timeout)
        return response

    def update_battery_by_id(self, battery_id: str, battery_update, timeout: float = 4.0) -> dict:
        response = self._fetch("put", f"/api/batman/v1/batteries/{battery_id}", data=battery_update, timeout=timeout)
        return response

    def remove_battery_by_id(self, battery_id: str, timeout: float = 4.0) -> dict:
        response = self._remove(f"/api/batman/v1/batteries/{battery_id}", timeout=timeout)
        return response

    def get_batteries(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/batteries", filter=filter, option=option, timeout=timeout)
        return response

    def get_batteries_count(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._get_json("/api/batman/v1/batteries/count", filter=filter, option=option, timeout=timeout)
        return response

    def get_children_of_battery_by_id(
        self, parent_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.parent": parent_battery_id}
        filter_with_id.update(filter)
        response = self._get_json("/api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_children_of_battery_by_id_count(
        self, parent_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.parent": parent_battery_id}
        filter_with_id.update(filter)
        response = self._fetch(
            "get", "/api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def get_leaves_of_battery_by_id(
        self, ancestor_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._get_json("/api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_leaves_of_battery_by_id_count(
        self, ancestor_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.is_leaf": True, "tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch(
            "get", "/api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    def get_decendants_of_battery_by_id(
        self, ancestor_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._get_json("/api/batman/v1/batteries", filter=filter_with_id, option=option, timeout=timeout)
        return response

    def get_decendants_of_battery_by_id_count(
        self, ancestor_battery_id: str, filter=None, option=None, timeout: float = 4.0
    ) -> dict:
        filter_with_id = {"tree.ancestors": ancestor_battery_id}
        filter_with_id.get(filter)
        response = self._fetch(
            "get", "/api/batman/v1/batteries/count", filter=filter_with_id, option=option, timeout=timeout
        )
        return response

    # ********************************************************
    # Section for the CapacityMeasurement
    # ********************************************************

    def create_capacity_measurement(self, capacity_measurement, timeout: float = 4.0) -> dict:
        response = self._post_json("/api/batman/v1/capacityMeasurements", data=capacity_measurement, timeout=timeout)
        return response

    def update_capacity_measurement_by_id(
        self, capacity_measurement_id: str, capacity_measurement, timeout: float = 4.0
    ) -> dict:
        response = self._fetch(
            "put",
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}",
            data=capacity_measurement,
            timeout=timeout,
        )
        return response

    def remove_capacity_measurement_by_id(self, capacity_measurement_id: str, timeout: float = 4.0) -> dict:
        response = self._fetch(
            "delete", f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}", timeout=timeout
        )
        return response

    def get_capacity_measurement(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._fetch(
            "get", "/api/batman/v1/capacityMeasurements", filter=filter, option=option, timeout=timeout
        )
        return response

    def get_capacity_measurement_count(self, filter=None, option=None, timeout: float = 4.0) -> dict:
        response = self._fetch(
            "get", "/api/batman/v1/capacityMeasurements/count", filter=filter, option=option, timeout=timeout
        )
        return response

    def get_capacity_measurement_by_id(self, capacity_measurement_id: str, timeout: float = 4.0) -> dict:
        response = self._get_json(f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}", timeout=timeout)
        return response

    def get_capacity_measurements_count_by_battery(self, battery_id: str, timeout: float = 4.0) -> dict:
        filter = {"battery._id": battery_id}
        response = self._get_json("/api/batman/v1/capacityMeasurements/count", filter=filter, timeout=timeout)
        return response

    def capacity_measurement_exists_on_remote(self, capacity_measurement_id, timeout: float = 4.0) -> dict:
        response = self._get_json(
            f"/api/batman/v1/capacityMeasurements/{capacity_measurement_id}", filter=filter, timeout=timeout
        )
        return response.id == capacity_measurement_id

    # ********************************************************
    # Section for the Measurements
    # ********************************************************

    def get_latests_measurement(self, device_id: str, count: int = 1, timeout: float = 4.0) -> dict:
        response = self._get_json(f"/api/batman/v1/devices/{device_id}/measurements/last/${count}", timeout=timeout)
        return response

    def write_device_measurements(self, device_measurements, timeout: float = 4.0) -> dict:
        response = self._post_json("/api/time-series/v1/measurements", data=device_measurements, timeout=timeout)
        return response
