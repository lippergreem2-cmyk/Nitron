import json
import sys
import urllib.request

ip = sys.argv[1] if len(sys.argv) > 1 else input("Enter IP address: ")

url = f"https://ipapi.co/{ip}/json/"

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)

    print("\n=== IP LOCATION ===")
    print("IP:       ", data.get("ip"))
    print("Country:  ", data.get("country_name"))
    print("Region:   ", data.get("region"))
    print("City:     ", data.get("city"))
    print("Timezone: ", data.get("timezone"))
    print("ISP:      ", data.get("org"))

except Exception as e:
    print("Lookup failed:", e)
