import requests
import json

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

    def get_device_list(self):
        method = "get"
        params = [{"url": "dvmdb/device"}]

        response = self._send_request(method, params)
        return response['result'][0]['data']

