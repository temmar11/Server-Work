import redfish
import time
from datetime import datetime

#server details
REDFISH_URL = "192.168.1.159"
USERNAME = "root"
PASSWORD = "calvin"

#define the loop control variable
continue_loop = True

#initialise redfish client
#simply put this logs you onto the redfish client and preps the space to be used in the code
try:
    client = redfish.redfish_client(base_url=REDFISH_URL, username=USERNAME, password=PASSWORD)
    while True:
        try:
            # Attempt to log in    
        

            client.login(auth="session")
            print("Successfully logged into the Redfish API")
            break  # Exit the loop if successful

        except redfish.rest.v1.SessionCreationError as e:
            client.logout()
            print("Logged out from Redfish API.11")
            time.sleep(5)  # Wait before retrying







            
    
        #Retrieve available systems
    systems_response = client.get("/redfish/v1/Systems")
    print("The System Status:", systems_response.status)
    if systems_response.status == 200:
        systems = systems_response.dict.get("Members", [])
        if not systems:
            print("No systems found.")
            continue_loop = False
        
        else:
            # Extract system ID from @odata.id
            system_data = systems[0]  # Get the first system
            SYSTEM_ID = system_data.get('@odata.id')
            print(f"Using System ID: {SYSTEM_ID}")  # Log the system ID
    i = 0

    user_input = input("Enter how many time you want to repeat the process: ")
    count = int(user_input)

    device_name = input("Enter the device name(s), separated by commas: ")
    device_name_string = [s.strip() for s in device_name.split(",")]



    for i in range(count):
        print("THIS IS i", i)
        #this will check the system status before turning on the server
        response = client.get(SYSTEM_ID)
        if response.status == 200:
            post_status = response.dict.get("Status", {}).get("State")
            print("Current System Status: {post_status}")

            if post_status == "Enabled":
                print("Server is already on")
                 #THIS NEEDS TO REMOVED AT ONE POINTaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            else:
                #This will power on the server
                power_action_url = "{SYSTEM_ID}/Actions/ComputerSystem.Reset"
                power_response = client.post(power_action_url, body={"ResetType": "On"})
                
            
                if power_response.status != 204:
                    print(power_response.status)
                    print("Failed to turn power on the server. Status: {power_response.status}, Response: {power_response.text}")
                    print(power_response.status)
                    break
                else:
                    print("Turning the server on...")
                    time.sleep(10)


        else:
            print("Error retrieving system status. Status Code: {response.text}")
            continue_loop = False
            break

        print("Preparing for Ethernet Interfaces (NICs)...")
        time.sleep(10)

        #Here we start the check for Ethernet Interfaces
        try:
            ethernet_response = client.get(f"{SYSTEM_ID}/EthernetInterfaces")
            if ethernet_response.status == 200:
                print("1")
                ethernet_interfaces = ethernet_response.dict.get("Members", [])
                if ethernet_interfaces:
                    print("NICs found")
                    for interface in ethernet_interfaces:
                        interface_url = interface.get('@odata.id')

                        #Fetches details for each NIC
                        interface_details_response = client.get(interface_url)
                        if interface_details_response.status == 200:
                            interface_id = interface_details_response.dict.get("Id")
                            interface_name = interface_details_response.dict.get("Name")
                            interface_mac = interface_details_response.dict.get("MACAddress")
                            print(f"ID: {interface_id}, Name: {interface_name}, MAC: {interface_mac}")
                        else:
                           print(f"Failed to retrieve details for NIC at {interface_url}. Status: {interface_details_response.status}")

                else:
                    print("No Ethernet Interfaces found")
            else:
               print(f"Failed to retrieve Ethernet interfaces. Status code: {ethernet_response.status}")

        except Exception as e:
            print(f"An error occurred while retrieving Ethernet interfaces: {e}")
        


finally:
# Ensure client logout
    try:
        client.logout()
        print("Logged out from Redfish API.222")
    except Exception as e:
        print(f"An error occurred while logging out: {e}")
