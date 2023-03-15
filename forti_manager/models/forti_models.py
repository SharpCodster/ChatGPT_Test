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


