def get_server_inventory(client):
    """
    Retrieve detailed information about the server, including hardware components.
    """
    try:
        system_endpoint = "/redfish/v1/Systems/System.Embedded.1"
        system_response = client.get(system_endpoint)

        if system_response.status == 200:
            system_data = system_response.dict
            # Prepare the inventory dictionary
            inventory = {
                "System": {
                    "Model": system_data.get("Model"),
                    "Manufacturer": system_data.get("Manufacturer"),
                    "Service Tag": system_data.get("SKU"),
                    "Serial Number": system_data.get("SerialNumber"),
                    "Memory Stick Count": get_memory_stick_count(client, system_data),  # Add memory stick count
                },
                "Processors": get_processor_data(client, system_data),
                "Memory": get_memory_data(client, system_data),
                "Hard Drives": get_hard_drive_data(client, system_data),
                "Network Cards": get_network_cards(client, system_data),
                "Controllers": get_controllers(client, system_data),
                "PCIe Devices": get_pcie_devices(client, system_data),
                "PowerState": system_data.get("PowerState"),
            }

            return inventory
        else:
            print(f"Failed to retrieve system information. HTTP Status: {system_response.status}")
            return None

    except Exception as e:
        print(f"An error occurred while retrieving server inventory: {e}")
        return None




def get_processor_data(client, system_data):
    """
    Retrieve detailed processor information.
    """
    try:
        processors_link = system_data.get("Processors", {}).get("@odata.id")
        
        if processors_link:
            processor_response = client.get(processors_link)
            if processor_response.status == 200:
                processor_data = processor_response.dict.get("Members", [])
          
                detailed_processors = []

                # Fetch details for each processor
                for processor in processor_data:
                    processor_detail_link = processor.get("@odata.id")
                    if processor_detail_link:
                        processor_detail_response = client.get(processor_detail_link)
                        if processor_detail_response.status == 200:
                            processor_detail = processor_detail_response.dict
                            detailed_processors.append({
                                "Model": processor_detail.get("Model"),
                                "Manufacturer": processor_detail.get("Manufacturer"),
                                "Max Speed MHz": processor_detail.get("MaxSpeedMHz"),
                                "Total Cores": processor_detail.get("TotalCores"),
                            })
                return detailed_processors
        else:
            print("Processors link not found.")
    except Exception as e:
        print(f"An error occurred while retrieving processor data: {e}")
    return []

def get_memory_data(client, system_data):
    """
    Retrieve detailed memory information by making requests to the @odata.id URLs.
    """
    try:
        memory_link = system_data.get("Memory", {}).get("@odata.id")

        if memory_link:
            memory_response = client.get(memory_link)
            if memory_response.status == 200:
                memory_data = memory_response.dict
                memory_members = memory_data.get("Members", [])
                detailed_memory = []

                for memory in memory_members:
                    memory_detail_link = memory.get("@odata.id")
                    if memory_detail_link:
                        memory_detail_response = client.get(memory_detail_link)
                        if memory_detail_response.status == 200:
                            memory_detail = memory_detail_response.dict
                            detailed_memory.append({
                                "Capacity MiB": memory_detail.get("CapacityMiB"),
                                "Type": memory_detail.get("MemoryDeviceType"),
                                "Speed MHz": memory_detail.get("OperatingSpeedMhz"),  
                                "Manufacturer": memory_detail.get("Manufacturer"),
                                "Part Number": memory_detail.get("PartNumber"),
                            })
                return detailed_memory
    except Exception as e:
        print(f"An error occurred while retrieving memory data: {e}")
    return []


def get_hard_drive_data(client, system_data):
    """
    Retrieve detailed hard drive information from the Storage endpoint.
    """
    try:
        storage_link = system_data.get("Storage", {}).get("@odata.id")

        if storage_link:
            storage_response = client.get(storage_link)
            if storage_response.status == 200:
                storage_data = storage_response.dict
                storage_members = storage_data.get("Members", [])
                detailed_drives = []

                for storage in storage_members:
                    storage_detail_link = storage.get("@odata.id")
                    if storage_detail_link:
                        storage_detail_response = client.get(storage_detail_link)
                        if storage_detail_response.status == 200:
                            storage_detail = storage_detail_response.dict
                            drives = storage_detail.get("Drives", [])
                            
                            for drive in drives:
                                drive_detail_link = drive.get("@odata.id")
                                if drive_detail_link:
                                    drive_detail_response = client.get(drive_detail_link)
                                    if drive_detail_response.status == 200:
                                        drive_detail = drive_detail_response.dict
                                        detailed_drives.append({
                                            "Model": drive_detail.get("Model"),
                                            "Manufacturer": drive_detail.get("Manufacturer"),
                                            "Capacity Bytes": drive_detail.get("CapacityBytes"),
                                            "Serial Number": drive_detail.get("SerialNumber"),
                                            "Media Type": drive_detail.get("MediaType"),
                                            "Status": drive_detail.get("Status", {}).get("Health"),
                                        })
                return detailed_drives
    except Exception as e:
        print(f"An error occurred while retrieving hard drive data: {e}")
    return []


def get_network_cards(client, system_data):
    """
    Retrieve detailed information about network cards/daughter cards.
    """
    try:
        network_link = system_data.get("NetworkInterfaces", {}).get("@odata.id")

        if network_link:
            network_response = client.get(network_link)
            if network_response.status == 200:
                network_data = network_response.dict
                network_members = network_data.get("Members", [])
                detailed_network_cards = []

                for network in network_members:
                    network_detail_link = network.get("@odata.id")
                    if network_detail_link:
                        network_detail_response = client.get(network_detail_link)
                        if network_detail_response.status == 200:
                            network_detail = network_detail_response.dict
                            detailed_network_cards.append({
                                "Name": network_detail.get("Name"),
                                "Manufacturer": network_detail.get("Manufacturer"),
                                "Model": network_detail.get("Model"),
                                "MAC Address": network_detail.get("MACAddress"),
                                "Speed Mbps": network_detail.get("SpeedMbps"),
                                "Status": network_detail.get("Status", {}).get("Health"),
                            })
                return detailed_network_cards
    except Exception as e:
        print(f"An error occurred while retrieving network cards: {e}")
    return []


def get_controllers(client, system_data):
    """
    Retrieve detailed information about controllers (e.g., RAID, storage).
    """
    try:
        storage_link = system_data.get("Storage", {}).get("@odata.id")

        if storage_link:
            storage_response = client.get(storage_link)
            if storage_response.status == 200:
                storage_data = storage_response.dict
                storage_members = storage_data.get("Members", [])
                detailed_controllers = []

                for storage in storage_members:
                    storage_detail_link = storage.get("@odata.id")
                    if storage_detail_link:
                        storage_detail_response = client.get(storage_detail_link)
                        if storage_detail_response.status == 200:
                            storage_detail = storage_detail_response.dict
                            controllers = storage_detail.get("StorageControllers", [])
                            
                            for controller in controllers:
                                detailed_controllers.append({
                                    "Name": controller.get("Name"),
                                    "Manufacturer": controller.get("Manufacturer"),
                                    "Model": controller.get("Model"),
                                    "Firmware Version": controller.get("FirmwareVersion"),
                                    "Status": controller.get("Status", {}).get("Health"),
                                })
                return detailed_controllers
    except Exception as e:
        print(f"An error occurred while retrieving controllers: {e}")
    return []


def get_pcie_devices(client, system_data):
    """
    Retrieve detailed PCIe device information and display essential fields only.
    """
    try:
        pcie_devices_link = system_data.get("PCIeDevices", [])

        if isinstance(pcie_devices_link, list):  # Ensure it's a list
            pcie_device_details = []
            for pcie_device in pcie_devices_link:
                if isinstance(pcie_device, dict):  # Ensure each item is a dictionary
                    device_detail_link = pcie_device.get("@odata.id")
                    if device_detail_link:
                        device_detail_response = client.get(device_detail_link)
                        if device_detail_response.status == 200:
                            device_detail = device_detail_response.dict
                            # Extract and append only the required fields
                            pcie_device_details.append({
                                "Name": device_detail.get("Name"),
                                "Status": device_detail.get("Status", {}).get("Health"),
                            })
            return pcie_device_details
        else:
            print("No PCIe devices found.")
            return []
    except Exception as e:
        print(f"An error occurred while retrieving PCIe devices: {e}")
        return []



def get_memory_stick_count(client, system_data):
    """
    Retrieve the number of memory sticks from the Memory resource.
    """
    try:
        memory_link = system_data.get("Memory", {}).get("@odata.id")

        if memory_link:
            memory_response = client.get(memory_link)
            if memory_response.status == 200:
                memory_data = memory_response.dict
                memory_members = memory_data.get("Members", [])
                memory_count = len(memory_members)
                return memory_count
        else:
            print("No Memory resource found.")
            return 0
    except Exception as e:
        print(f"An error occurred while retrieving memory stick count: {e}")
        return 0
