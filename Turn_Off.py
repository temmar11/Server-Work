# Turn_Off.py
def power_off_server(client):
    power_off_endpoint = "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "GracefulShutdown"}
    response = client.post(power_off_endpoint, body=payload)

    if response.status in (200, 204):
        print("Server shutdown initiated successfully.")
    else:
        print(f"Failed to power off the server. Status code: {response.status}, Error: {response.text}")
