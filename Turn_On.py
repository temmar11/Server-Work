# Turn_On.py
def power_on_server(client):
    power_on_endpoint = "/redfish/v1/Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "On"}
    response = client.post(power_on_endpoint, body=payload)

    if response.status in (200, 204):
        print("Server power-on initiated successfully.")
    else:
        print(f"Failed to power on the server. Status code: {response.status}, Error: {response.text}")
