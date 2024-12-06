import redfish
import time
from datetime import datetime

# Server details
REDFISH_URL = "192.168.1.159"
USERNAME = "root"
PASSWORD = "calvin"


client = redfish.redfish_client(base_url=REDFISH_URL, username=USERNAME, password=PASSWORD)

try:
    client.logout()
    print("Logged out from Redfish API.")
except Exception as e:
    print(f"An error occurred while logging out: {e}")
