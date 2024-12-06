def full_health_check(client):
    system_endpoint = "/redfish/v1/Systems/System.Embedded.1"
    system_response = client.get(system_endpoint)
    if system_response.status == 200:
        system_data = system_response.dict

        health_check = {
            "Disk Health": check_disk_health(client, system_data),
            "Thermal Status": check_thermal_status(client),
            "CPU Health": check_cpu_health(client, system_data),
            "Firmware Details": get_firmware_details(client),
            "Power Supply Status": check_power_supply_status(client),
            "Network Status": check_network_status(client, system_data),
        }

        return health_check
    else:
        print(f"Failed to retrieve system data. HTTP Status: {system_response.status}")
        return None


def check_disk_health(client, system_data):
    """
    Perform health checks for all disks in the server.
    """
    try:
        storage_link = system_data.get("Storage", {}).get("@odata.id")

        if storage_link:
            storage_response = client.get(storage_link)
            if storage_response.status == 200:
                storage_data = storage_response.dict
                storage_members = storage_data.get("Members", [])
                disk_health = []

                for storage in storage_members:
                    storage_detail_link = storage.get("@odata.id")
                    if storage_detail_link:
                        storage_detail_response = client.get(storage_detail_link)
                        if storage_detail_response.status == 200:
                            storage_detail = storage_detail_response.dict
                            for drive in storage_detail.get("Drives", []):
                                drive_detail_link = drive.get("@odata.id")
                                if drive_detail_link:
                                    drive_detail_response = client.get(drive_detail_link)
                                    if drive_detail_response.status == 200:
                                        drive_detail = drive_detail_response.dict
                                        disk_health.append({
                                            "Model": drive_detail.get("Model"),
                                            "SerialNumber": drive_detail.get("SerialNumber"),
                                            "Health": drive_detail.get("Status", {}).get("Health"),
                                            "Temperature (C)": drive_detail.get("Oem", {}).get("Dell", {}).get("TemperatureCelsius"),
                                            "Capacity (Bytes)": drive_detail.get("CapacityBytes"),
                                        })
                return disk_health
        return []
    except Exception as e:
        print(f"An error occurred while checking disk health: {e}")
        return []


def check_thermal_status(client):
    """
    Perform thermal checks, including temperature and fan speeds.
    """
    try:
        thermal_endpoint = "/redfish/v1/Chassis/System.Embedded.1/Thermal"
        thermal_response = client.get(thermal_endpoint)
        if thermal_response.status == 200:
            thermal_data = thermal_response.dict

            temperatures = thermal_data.get("Temperatures", [])
            fans = thermal_data.get("Fans", [])

            thermal_status = {
                "Temperatures": [
                    {"Name": temp.get("Name"), "ReadingC": temp.get("ReadingCelsius"), "Health": temp.get("Status", {}).get("Health")}
                    for temp in temperatures
                ],
                "Fans": [
                    {"Name": fan.get("Name"), "SpeedRPM": fan.get("Reading"), "Health": fan.get("Status", {}).get("Health")}
                    for fan in fans
                ]
            }
            return thermal_status
        return {}
    except Exception as e:
        print(f"An error occurred while checking thermal status: {e}")
        return {}


def check_cpu_health(client, system_data):
    """
    Check the health and utilization of the server's CPUs.
    """
    try:
        processors_link = system_data.get("Processors", {}).get("@odata.id")

        if processors_link:
            processors_response = client.get(processors_link)
            if processors_response.status == 200:
                processors_data = processors_response.dict.get("Members", [])
                cpu_health = []

                for processor in processors_data:
                    processor_detail_link = processor.get("@odata.id")
                    if processor_detail_link:
                        processor_detail_response = client.get(processor_detail_link)
                        if processor_detail_response.status == 200:
                            processor_detail = processor_detail_response.dict
                            cpu_health.append({
                                "Model": processor_detail.get("Model"),
                                "Total Cores": processor_detail.get("TotalCores"),
                                "Health": processor_detail.get("Status", {}).get("Health"),
                            })
                return cpu_health
        return []
    except Exception as e:
        print(f"An error occurred while checking CPU health: {e}")
        return []


def get_firmware_details(client):
    """
    Retrieve firmware details for the server.
    """
    try:
        firmware_endpoint = "/redfish/v1/UpdateService/FirmwareInventory"
        firmware_response = client.get(firmware_endpoint)


        if firmware_response.status == 200:
            firmware_data = firmware_response.dict.get("Members", [])
            firmware_details = []

            for firmware in firmware_data:
                firmware_detail_link = firmware.get("@odata.id")
                if firmware_detail_link:
                    firmware_detail_response = client.get(firmware_detail_link)
                    if firmware_detail_response.status == 200:
                        firmware_detail = firmware_detail_response.dict
                        firmware_details.append({
                            "Name": firmware_detail.get("Name"),
                            "Version": firmware_detail.get("Version"),
                            "Updateable": firmware_detail.get("Updateable"),
                        })
            return firmware_details
        else:
            print(f"Failed to retrieve firmware details. HTTP Status: {firmware_response.status}")
        return []
    except Exception as e:
        print(f"An error occurred while retrieving firmware details: {e}")
        return []


def check_power_supply_status(client):
    """
    Check power supply health and redundancy.
    """
    try:
        power_endpoint = "/redfish/v1/Chassis/System.Embedded.1/Power"
        power_response = client.get(power_endpoint)
        if power_response.status == 200:
            power_data = power_response.dict.get("PowerSupplies", [])
            power_status = [
                {
                    "Name": supply.get("Name"),
                    "Health": supply.get("Status", {}).get("Health"),
                    "PowerOutputWatts": supply.get("LastPowerOutputWatts"),
                }
                for supply in power_data
            ]
            return power_status
        return []
    except Exception as e:
        print(f"An error occurred while checking power supply status: {e}")
        return []


def check_network_status(client, system_data):
    """
    Retrieve the status of network cards and connectivity.
    """
    try:
        network_link = system_data.get("NetworkInterfaces", {}).get("@odata.id")

        if network_link:
            network_response = client.get(network_link)

            if network_response.status == 200:
                network_data = network_response.dict.get("Members", [])
                network_status = []

                for network in network_data:
                    network_detail_link = network.get("@odata.id")
                    if network_detail_link:
                        network_detail_response = client.get(network_detail_link)
                        if network_detail_response.status == 200:
                            network_detail = network_detail_response.dict
                            network_status.append({
                                "Name": network_detail.get("Name"),
                                "MAC Address": network_detail.get("MACAddress"),
                                "SpeedMbps": network_detail.get("SpeedMbps"),
                                "Health": network_detail.get("Status", {}).get("Health"),
                            })
                return network_status
        else:
            print("No network interfaces link found in system data.")
        return []
    except Exception as e:
        print(f"An error occurred while checking network status: {e}")
        return []
