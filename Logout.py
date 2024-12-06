import redfish
import time
from client import create_redfish_client

# Logout.py
def logout():
    client = create_redfish_client()
    try:
        client.logout()
        print("Logged out from Redfish API.")
    except Exception as e:
        print(f"An error occurred while logging out: {e}")





