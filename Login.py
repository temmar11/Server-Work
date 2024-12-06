
import redfish
import time

# Login.py
def login(client):
    while True:
        try:
            client.login(auth="session")
            print("Successfully logged into the Redfish API.")
            break
        except redfish.rest.v1.SessionCreationError:
            client.logout()
            print("Session creation failed. Retrying...")
            time.sleep(5)  # Retry after a short delay
