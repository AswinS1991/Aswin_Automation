from api.devices import get_customer_devices

ORG_ID = ""

def monitor():

    print("Fetching devices...")

    devices = get_customer_devices(ORG_ID)

    print(f"Total Devices Retrieved: {len(devices)}")

    for device in devices[:10]:

        name = device.get(
            "displayName",
            "Unknown"
        )

        status = device.get(
            "connectionStatus",
            "unknown"
        )

        print(name, "-->", status)

if __name__ == "__main__":

    monitor()

    input("Press Enter to exit...")
