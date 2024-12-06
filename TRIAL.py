import redfish
import time
from Login import login
from client import create_redfish_client
from Logout import logout
from Retrieve_Systems_Status import retrieveSystemStatus


def CheckServerOnOff():
    # Create the Redfish client
    client = create_redfish_client()
def check_server_power_state():
    # Create the client and log in
    client = create_redfish_client()
    try:
        client.login(auth="session")  # Use session-based authentication
        
        # Define the endpoint for querying system info
        systems_endpoint = "/redfish/v1/Systems/System.Embedded.1"
        
        # Send the GET request
        response = client.get(systems_endpoint)
        
        # Check the response status
        if response.status == 200:
            # Parse the response and extract PowerState
            response_body = response.dict  # Redfish library provides .dict for JSON responses
            power_state = response_body.get("PowerState", "Unknown")
            print(f"PowerState of the server: {power_state}")
            return power_state
        else:
            print(f"Failed to retrieve server status. HTTP Status: {response.status}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure the client logs out
        client.logout()

# Call the function to check the power state
power_state = check_server_power_state()