"""
ip_finder.py
Looks up geolocation and network info for an IP address using the
free ipinfo.io API. Get a free API token at https://ipinfo.io
(free tier covers casual/personal use).
"""

import requests

API_KEY = "YOUR_API_KEY"  # replace with your ipinfo.io token


def get_ip_info(ip: str) -> dict:
    url = f"https://ipinfo.io/{ip}?token={API_KEY}"
    response = requests.get(url)
    return response.json()


def print_report(data: dict):
    print("\nIP LOOKUP RESULT")
    print(f"  IP Address : {data.get('ip', 'N/A')}")
    print(f"  Country    : {data.get('country', 'N/A')}")
    print(f"  Region     : {data.get('region', 'N/A')}")
    print(f"  City       : {data.get('city', 'N/A')}")
    print(f"  Location   : {data.get('loc', 'N/A')}")
    print(f"  ISP/Org    : {data.get('org', 'N/A')}")
    print(f"  Timezone   : {data.get('timezone', 'N/A')}")


if __name__ == "__main__":
    ip = input("Enter an IP address: ").strip()
    data = get_ip_info(ip)
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print_report(data)
