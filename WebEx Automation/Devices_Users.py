import requests
from config import ACCESS_TOKEN

url = "https://webexapis.com/v1/devices"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

print("Fetching devices...\n")

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error : {response.status_code}")
    print(response.text)
    exit()

devices = response.json()["items"]

print(f"Total Devices : {len(devices)}\n")

print("{:<45} {}".format("DEVICE NAME", "STATUS"))
print("-" * 65)

for device in devices:

    name = (
        device.get("displayName")
        or device.get("personDisplayName")
        or "Unknown Device"
    )

    status = device.get("connectionStatus", "Unknown")

    print("{:<45} {}".format(name, status))
    
    

# Fetch Users
# ==================================================

print("\n\nFetching users...\n")

url = "https://webexapis.com/v1/people"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error fetching users : {response.status_code}")
    print(response.text)
else:

    users = response.json()["items"]

    print(f"Total Users : {len(users)}\n")

    print("{:<35}{:<40}{}".format(
        "DISPLAY NAME",
        "EMAIL",
        "STATUS"
    ))

    print("-" * 95)

    for user in users:

        display_name = user.get("displayName", "N/A")

        emails = user.get("emails", [])
        email = emails[0] if emails else "N/A"

        status = user.get("status", "Unknown")

        print("{:<35}{:<40}{}".format(
            display_name,
            email,
            status
        ))
input("\nPress Enter to exit...")
