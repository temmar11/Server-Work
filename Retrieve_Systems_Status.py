
import redfish
import time
from Login import login
from client import create_redfish_client
from Logout import logout

def retrieveSystemStatus():
    # Calls on the "Login" function which will logon to the server
    login()

    
    
    client = create_redfish_client()
    

    #This section will retrieve the avalable systems

    while True:
        systems_response = client.get("/redfish/v1/Systems")
        print("The System Status: ", systems_response.status)
        systems_response_status = systems_response.status
        if systems_response_status == 200:
            systems = systems_response.dict.get("Members, []")
            if not systems:
                print("No systems found.")
                break
            else:
                # this will extract system ID from @odata.id
                system_data = systems[0] # this will 192.168.1.159get the first system
                SYSTEM_ID = system_data.get('@odata.id')   # this variable might need to be turned into a global variable not sure
                print(f"Using System ID: {SYSTEM_ID}")    # This will log the system ID



    return systems_response_status

