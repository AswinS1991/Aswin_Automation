from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.helpers import serialize_object

# ==================================================
# Five9 Credentials
# ==================================================

USERNAME = "API enabled Username"
PASSWORD = "Password"

WSDL = (
    "https://api.five9.com/wsadmin/v13/"
    "AdminWebService?wsdl&user="
    + USERNAME
)

# ==================================================
# Connect to Five9
# ==================================================

session = Session()
session.auth = HTTPBasicAuth(USERNAME, PASSWORD)

client = Client(
    wsdl=WSDL,
    transport=Transport(session=session)
)

print("Connected Successfully")

# ==================================================
# User Input
# ==================================================

search_number = input("\nEnter DNIS Number: ").strip()

campaigns = client.service.getCampaigns()

found = False

for campaign in campaigns:

    # Only inbound campaigns have DNIS
    if campaign.type != "INBOUND":
        continue

    try:

        dnis_list = client.service.getCampaignDNISList(
            campaign.name
        )

        if search_number in dnis_list:

            found = True

            details = client.service.getInboundCampaign(
                campaign.name
            )

            #print("\nFULL SERIALIZED CAMPAIGN OBJECT")
            #print("=" * 80)

            data = serialize_object(details)
            #print(data)

            print("=" * 80)

            print("\nMATCH FOUND")
            print("-" * 60)
            print(f"Campaign : {details.name}")
            print(f"Type     : {details.type}")
            print(f"State    : {details.state}")
            print(f"Profile  : {details.profileName}")

            try:
                ivr_name = (
                    details.defaultIvrSchedule
                    .ivrSchedule
                    .scriptName
                )

                print(f"Default IVR : {ivr_name}")

            except Exception as e:

                print(f"Default IVR Error: {e}")

            print("-" * 60)

            break

    except Exception as e:

        print(f"ERROR on campaign {campaign.name}: {e}")

if not found:
    print("\nNumber not found.")

input("\nPress Enter to exit...")