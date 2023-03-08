"""
_summary_
"""

from pydantic import BaseModel


class DeviceEvent(BaseModel):
    """
    _summary_
    """

    device_name: str
    event_type: str
    timestamp: int


class DeviceCounter(BaseModel):
    """
    _summary_
    """

    device_name: str
    counter_type: str
    value: int


class DeviceInfo(BaseModel):
    """
    _summary_
    """

    name: str
    serial_number: str
    os_version: str
    cpu_usage: float
    memory_usage: float
    events: list[DeviceEvent]
    counters: list[DeviceCounter]


class CustomerDeviceInfo(BaseModel):
    """
    _summary_
    """

    customer_name: str
    devices: list[DeviceInfo]
