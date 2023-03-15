
from forti_manager.forti_manager_client import FortiManagerAPI

username = input("Please enter your username: ")
password = input("Please enter your password: ")
base_url = input("Please enter FortiManager Url: ")



fmg_api = FortiManagerAPI(host=base_url, username=username, password=password)
device_list = fmg_api.get_device_list()
for device in device_list:
    print(device)
fmg_api.logout()

