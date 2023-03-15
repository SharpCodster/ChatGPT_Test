import requests
import json
from typing import List

from forti_manager.models.forti_models import Device, PolicyPackage, ADOM


class FortiManagerAPI:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.base_url = f"https://{self.host}/jsonrpc"
        self.session = requests.Session()
        self.login()

    def _send_request(self, method, params=None, include_session=True):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "method": method,
            "params": params or [],
            "id": 1,
            "jsonrpc": "2.0"
        }
        
        if include_session:
            payload["session"] = self.session_id

        response = self.session.post(self.base_url, headers=headers, data=json.dumps(payload), verify=False)
        response.raise_for_status()

        return response.json()

    def login(self):
        method = "exec"
        params = [{
            "url": "sys/login/user",
            "data": {
                "user": self.username,
                "passwd": self.password
            }
        }]

        response = self._send_request(method, params, include_session=False)
        self.session_id = response['session']

    def logout(self):
        method = "exec"
        params = [{"url": "sys/logout"}]

        self._send_request(method, params)
        self.session.close()

    def get_device_list(self) -> List[Device]:
        method = "get"
        params = [{"url": "dvmdb/device"}]

        response = self._send_request(method, params)
        device_data = response['result'][0]['data']
        devices = [Device(**device) for device in device_data]

        return devices
    
    def get_policy_package_list(self) -> List[PolicyPackage]:
        method = "get"
        params = [{"url": "pm/pkg"}]

        response = self._send_request(method, params)
        package_data = response['result'][0]['data']
        packages = [PolicyPackage(**package) for package in package_data]

        return packages
    
    def get_adom_list(self) -> List[ADOM]:
        method = "get"
        params = [{"url": "dvmdb/adom"}]

        response = self._send_request(method, params)
        adom_data = response['result'][0]['data']
        adoms = [ADOM(**adom) for adom in adom_data]

        return adoms

