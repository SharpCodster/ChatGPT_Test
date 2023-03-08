
from forti_manager.forti_manager_client import SBFortiManager

username = input("Please enter your username: ")
password = input("Please enter your password: ")
base_url = input("Please enter FortiManager Url: ")


api = SBFortiManager(base_url, username, password)
customers = api.get_customers()



