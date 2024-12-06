import re
import redfish


client = None

def validate_url(url):
    pattern = r'^(https?://)?([a-zA-Z0-9.-]+)(:\d+)?(/.*)?$'
    return re.match(pattern, url) is not None

def create_redfish_client():
    global client
    if client is None:
        while True:
            REDFISH_URL = input("Enter the Redfish URL: ").strip()
            if not validate_url(REDFISH_URL):
                print("Invalid URL format. Please enter a valid URL.")
                continue
            if not REDFISH_URL.startswith("http://") and not REDFISH_URL.startswith("https://"):
                REDFISH_URL = "https://" + REDFISH_URL  # Default to HTTPS if no scheme is provided
            break

        USERNAME = input("Enter the user name: ").strip()
        PASSWORD = input("Enter the Password: ").strip()
        client = redfish.redfish_client(base_url=REDFISH_URL, username=USERNAME, password=PASSWORD)
    return client
