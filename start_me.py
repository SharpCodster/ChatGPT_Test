
from forti_manager.forti_manager_client import FortiManagerAPI

username = input("Please enter your username: ")
password = input("Please enter your password: ")
base_url = input("Please enter FortiManager Url: ")



fmg_api = FortiManagerAPI(host=base_url, username=username, password=password)

device_list = fmg_api.get_device_list()
for device in device_list:
    print(device)

adom_list = fmg_api.get_adom_list()
for adom in adom_list:
    print(adom)

policy_package_list = fmg_api.get_policy_package_list()
for policy in policy_package_list:
    print(policy)


fmg_api.logout()

