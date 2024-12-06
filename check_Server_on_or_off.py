# check_Server_on_or_off.py
def check_server_power_state(client):
    try:
        systems_endpoint = "/redfish/v1/Systems/System.Embedded.1"
        response = client.get(systems_endpoint)

        if response.status == 200:
            power_state = response.dict.get("PowerState", "Unknown")
            return power_state
        else:
            print(f"Failed to retrieve server status. HTTP Status: {response.status}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
