"""
_summary_
"""

from pydantic import BaseModel
from typing import Optional

class Device(BaseModel):
    adom: Optional[str]
    desc: str
    ip: str
    name: str
    os_type: str
    os_ver: str


class PolicyPackage(BaseModel):
    adom: Optional[str]
    name: str
    scope: str

class ADOM(BaseModel):
    name: str
    desc: Optional[str]
    flags: Optional[int]
    os_ver: Optional[str]
