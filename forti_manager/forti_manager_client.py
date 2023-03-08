"""
_summary_

Returns:
    _type_: _description_
"""

from ast import List

import requests

from forti_manager.models.forti_models import (
    DeviceCounter,
    DeviceEvent,
    DeviceInfo,
    CustomerDeviceInfo,
)

from typing import TypeVar, Type
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


def from_json(json_data: dict, model_class: Type[ModelType]) -> ModelType:
    """
    Convert a dictionary of JSON data to a Pydantic model object.
    """
    return model_class(**json_data)


class SBFortiManager:
    """
    Forti manager API Operations
    """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_token(self):
        """
        _summary_
        """
        url = f"{self.base_url}/sys/login/user"
        payload = {"user": self.username, "passwd": self.password}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["session"]

    def get_customers(self) -> list[CustomerDeviceInfo]:
        """
        Retrieve a list of all customers associated with the user's account.
        """

        url = f"{self.base_url}/dvmdb/adom"
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        customers = response.json()

        customer_device_info_list = []
        for customer in customers:
            devices = self.get_devices_for_customer(customer["name"])
            customer_device_info = CustomerDeviceInfo(
                customer_name=customer["name"], devices=[]
            )
            customer_device_info_list.append(customer_device_info)
        return customer_device_info_list

    def get_devices_for_customer(self, customer):
        """
        _summary_
        """
        url = f"{self.base_url}/dvmdb/adom/{customer}/device"
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = []
        for device_json in response.json():
            device = DeviceInfo(
                name=device_json["name"],
                serial_number=device_json["serial"],
                os_version=device_json["os_version"],
                cpu_usage=device_json["cpu"],
                memory_usage=device_json["memory"],
                events=[],
                counters=[],
            )
            devices.append(device)
        return devices

    def get_device_info(self, customer, device):
        """
        _summary_
        """
        url = f"{self.base_url}/dvmdb/adom/{customer}/device/{device}"

        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        device_info_dict = response.json()
        device_events = [
            from_json(event_data, DeviceEvent)
            for event_data in device_info_dict["events"]
        ]
        device_counters = [
            from_json(counter_data, DeviceCounter)
            for counter_data in device_info_dict["counters"]
        ]
        device_info = from_json(
            {
                "name": device_info_dict["name"],
                "serial_number": device_info_dict["serial"],
                "os_version": device_info_dict["os_version"],
                "cpu_usage": device_info_dict["cpu"],
                "memory_usage": device_info_dict["memory"],
                "events": device_events,
                "counters": device_counters,
            },
            DeviceInfo,
        )
        return device_info
