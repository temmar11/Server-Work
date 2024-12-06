import tkinter as tk
from tkinter import messagebox, scrolledtext
from client import create_redfish_client
from Logout import logout
from Login import login
from check_Server_on_or_off import check_server_power_state
from Turn_Off import power_off_server
from Turn_On import power_on_server
from Inventory import get_server_inventory
from HealthChecks import full_health_check


class RedfishServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Redfish Server Monitoring Tool")
        self.root.geometry("800x600")

        # Redfish Client
        self.client = None

        # Login Frame
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Redfish URL:").grid(row=0, column=0, sticky="e", padx=5)
        self.url_entry = tk.Entry(self.login_frame, width=40)
        self.url_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.login_frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5)
        self.username_entry = tk.Entry(self.login_frame, width=40)
        self.username_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.login_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5)
        self.password_entry = tk.Entry(self.login_frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, padx=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login_to_redfish)
        self.login_button.grid(row=3, columnspan=2, pady=10)

        # Main Frame (Disabled until login)
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=10)
        self.main_frame.pack_forget()

        # Labels to display information
        self.status_label = tk.Label(self.main_frame, text="Server Status: N/A", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Buttons for user actions
        self.check_power_button = tk.Button(self.main_frame, text="Check Server Power", command=self.check_server_power)
        self.check_power_button.pack(pady=5)

        self.get_inventory_button = tk.Button(self.main_frame, text="Get Server Inventory", command=self.get_server_inventory)
        self.get_inventory_button.pack(pady=5)

        self.health_check_button = tk.Button(self.main_frame, text="Check Server Health", command=self.check_server_health)
        self.health_check_button.pack(pady=5)

        self.power_off_button = tk.Button(self.main_frame, text="Power OFF Server", command=self.power_off_server)
        self.power_off_button.pack(pady=5)

        self.power_on_button = tk.Button(self.main_frame, text="Power ON Server", command=self.power_on_server)
        self.power_on_button.pack(pady=5)

        # Text box to display detailed results
        self.result_text = scrolledtext.ScrolledText(self.main_frame, height=20, width=80)
        self.result_text.pack(pady=10)

    def login_to_redfish(self):
        """
        Log in to Redfish API using user-provided credentials.
        """
        redfish_url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not redfish_url or not username or not password:
            messagebox.showwarning("Missing Fields", "Please enter all login details.")
            return

        try:
            from redfish import redfish_client
            self.client = redfish_client(base_url=redfish_url, username=username, password=password)
            self.client.login(auth="session")
            messagebox.showinfo("Login Successful", "Successfully logged into the Redfish API.")

            # Enable the main UI
            self.main_frame.pack()
            self.login_frame.pack_forget()

        except Exception as e:
            messagebox.showerror("Login Failed", f"Failed to login: {e}")

    def check_server_power(self):
        """
        Check and display server power state.
        """
        try:
            power_state = check_server_power_state(self.client)
            if power_state == "On":
                self.status_label.config(text="Server is ON")
            elif power_state == "Off":
                self.status_label.config(text="Server is OFF")
            else:
                self.status_label.config(text="Unable to determine power state")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to check server power state: {e}")

    def get_server_inventory(self):
        """
        Retrieve and display server inventory.
        """
        try:
            inventory = get_server_inventory(self.client)
            if inventory:
                report = "\n--- Server Inventory ---\n"
                for key, value in inventory.items():
                    report += f"{key}: {value}\n"
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, report)
            else:
                messagebox.showwarning("Warning", "Failed to retrieve inventory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving inventory: {e}")

    def check_server_health(self):
        """
        Perform and display server health check.
        """
        try:
            # Perform the full health check
            health_report = full_health_check(self.client)

            if health_report:
                # Build the report string
                report = "\n--- Full Server Health Report ---\n"

                # Disk Health
                report += "\nDisk Health:\n"
                for disk in health_report.get("Disk Health", []):
                    report += (f"  Model: {disk['Model']}, Serial: {disk['SerialNumber']}, "
                               f"Health: {disk['Health']}, Temperature: {disk['Temperature (C)']}°C, "
                               f"Capacity: {disk['Capacity (Bytes)']} Bytes\n")

                # Thermal Status
                thermal_status = health_report.get("Thermal Status", {})
                report += "\nThermal Status:\n  Temperatures:\n"
                for temp in thermal_status.get("Temperatures", []):
                    report += f"    {temp['Name']}: {temp['ReadingC']}°C (Health: {temp['Health']})\n"
                report += "  Fans:\n"
                for fan in thermal_status.get("Fans", []):
                    report += f"    {fan['Name']}: {fan['SpeedRPM']} RPM (Health: {fan['Health']})\n"

                # CPU Health
                report += "\nCPU Health:\n"
                for cpu in health_report.get("CPU Health", []):
                    report += (f"  Model: {cpu['Model']}, Total Cores: {cpu['Total Cores']}, "
                               f"Health: {cpu['Health']}\n")

                # Firmware Details
                report += "\nFirmware Details:\n"
                for firmware in health_report.get("Firmware Details", []):
                    report += (f"  Name: {firmware['Name']}, Version: {firmware['Version']}, "
                               f"Updateable: {firmware['Updateable']}\n")

                # Power Supply Status
                report += "\nPower Supply Status:\n"
                for supply in health_report.get("Power Supply Status", []):
                    report += (f"  Name: {supply['Name']}, Health: {supply['Health']}, "
                               f"Power Output: {supply['PowerOutputWatts']} Watts\n")

                # Network Status
                report += "\nNetwork Status:\n"
                for network in health_report.get("Network Status", []):
                    report += (f"  Name: {network['Name']}, MAC: {network['MAC Address']}, "
                               f"Speed: {network['SpeedMbps']} Mbps (Health: {network['Health']})\n")

                # Update the text box with the health report
                self.result_text.delete(1.0, tk.END)  # Clear previous results
                self.result_text.insert(tk.END, report)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Failed to retrieve health report.")
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error during health check: {e}")

    def power_off_server(self):
        """
        Power off the server.
        """
        try:
            power_off_server(self.client)
            messagebox.showinfo("Power Off", "Server power-off command sent.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to power off server: {e}")

    def power_on_server(self):
        """
        Power on the server.
        """
        try:
            power_on_server(self.client)
            messagebox.showinfo("Power On", "Server power-on command sent.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to power on server: {e}")


# Entry point
def main():
    root = tk.Tk()
    app = RedfishServerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
