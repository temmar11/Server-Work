import redfish
from client import create_redfish_client
from Logout import logout
from Login import login
from check_Server_on_or_off import check_server_power_state
from Turn_Off import power_off_server
from Turn_On import power_on_server
from Inventory import get_server_inventory
from HealthChecks import full_health_check 

def main():
    # Step 1: Create Redfish client
    client = create_redfish_client()
    login(client)

    try:
        # Step 2: Check server power state
        power_state = check_server_power_state(client)

        if power_state == "On":
            print("Server is already ON.")
        elif power_state == "Off":
            print("Server is currently OFF.")
            turn_on_choice = input("Would you like to turn the server ON? (Y/N): ").strip().lower()

            if turn_on_choice == "y":
                power_on_server(client)
            elif turn_on_choice == "n":
                print("Server will remain OFF.")
            else:
                print("Invalid input. No action taken.")
        else:
            print("Unable to determine server power state.")

        # Step 3: Retrieve and display server inventory
        inventory = get_server_inventory(client)
        if inventory:
            print("\nServer Inventory:")
            for key, value in inventory.items():
                print(f"{key}: {value}")
        else:
            print("Failed to retrieve server inventory.")

        # Step 4: Ask if user wants to run a health check
        health_check_choice = input("Would you like to run a full health check? (Y/N): ").strip().lower()
        if health_check_choice == "y":
            print("\nRunning Full Health Check...")
            health_report = full_health_check(client)
            if health_report:
                print("\n--- Full Server Health Report ---")
                print("\nDisk Health:")
                for disk in health_report.get("Disk Health", []):
                    print(f"  Model: {disk['Model']}, Serial: {disk['SerialNumber']}, "
                          f"Health: {disk['Health']}, Temperature: {disk['Temperature (C)']}, "
                          f"Capacity: {disk['Capacity (Bytes)']} Bytes")

                print("\nThermal Status:")
                print("  Temperatures:")
                for temp in health_report.get("Thermal Status", {}).get("Temperatures", []):
                    print(f"    {temp['Name']}: {temp['ReadingC']}°C (Health: {temp['Health']})")
                print("  Fans:")
                for fan in health_report.get("Thermal Status", {}).get("Fans", []):
                    print(f"    {fan['Name']}: {fan['SpeedRPM']} RPM (Health: {fan['Health']})")

                print("\nCPU Health:")
                for cpu in health_report.get("CPU Health", []):
                    print(f"  Model: {cpu['Model']}, Total Cores: {cpu['Total Cores']}, "
                          f"Health: {cpu['Health']}")

                print("\nFirmware Details:")
                for firmware in health_report.get("Firmware Details", []):
                    print(f"  Name: {firmware['Name']}, Version: {firmware['Version']}, "
                          f"Updateable: {firmware['Updateable']}")

                print("\nPower Supply Status:")
                for supply in health_report.get("Power Supply Status", []):
                    print(f"  Name: {supply['Name']}, Health: {supply['Health']}, "
                          f"Power Output: {supply['PowerOutputWatts']} Watts")

                print("\nNetwork Status:")
                for network in health_report.get("Network Status", []):
                    print(f"  Name: {network['Name']}, MAC: {network['MAC Address']}, "
                          f"Speed: {network['SpeedMbps']} Mbps (Health: {network['Health']})")
            else:
                print("Failed to retrieve health report.")
        elif health_check_choice == "n":
            print("Skipping health check.")
        else:
            print("Invalid input. Skipping health check.")

        # Optional Step: Power off the server (if required)
        power_off_choice = input("Would you like to power OFF the server? (Y/N): ").strip().lower()
        if power_off_choice == "y":
            power_off_server(client)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Step 5: Logout
        logout()
        print("Logged out successfully.")

# Entry point
if __name__ == "__main__":
    main()
