import json
import subprocess
import requests
import webbrowser

print("""
╔══════════════════════════════════════╗
║          NITRON GPS MAP              ║
╠══════════════════════════════════════╣
║       DEVICE LOCATION LOOKUP         ║
╚══════════════════════════════════════╝
""")

try:
    # Get GPS location from this device
    result = subprocess.run(
        ["termux-location"],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode != 0:
        print("❌ Could not get GPS location.")
        print(result.stderr)
        raise SystemExit

    data = json.loads(result.stdout)

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    accuracy = data.get("accuracy")

    if latitude is None or longitude is None:
        print("❌ GPS coordinates were not returned.")
        raise SystemExit

    print("📍 Latitude: ", latitude)
    print("📍 Longitude:", longitude)
    print("🎯 Accuracy: ", accuracy, "meters")

    # Reverse geocode coordinates
    url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "jsonv2",
        "zoom": 18,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": "Nitron-GPS-Map/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    place = response.json()
    address = place.get("address", {})

    print("\n========== LOCATION ==========")

    print("🏠 Exact place:",
          place.get("display_name", "Unknown"))

    print("🏙️ Town/City:",
          address.get("city")
          or address.get("town")
          or address.get("municipality")
          or address.get("village")
          or "Unknown")

    print("🏛️ County:",
          address.get("county")
          or address.get("state_district")
          or "Unknown")

    print("🌍 Country:",
          address.get("country", "Unknown"))

    print("==============================")

    # Open exact coordinates on OpenStreetMap
    map_url = (
        "https://www.openstreetmap.org/"
        f"?mlat={latitude}&mlon={longitude}"
        f"#map=19/{latitude}/{longitude}"
    )

    print("\n🗺️ Opening exact GPS position...")
    webbrowser.open(map_url)

except subprocess.TimeoutExpired:
    print("❌ GPS request timed out.")

except requests.RequestException as e:
    print("❌ Map lookup failed:", e)

except json.JSONDecodeError:
    print("❌ Invalid GPS response.")

except Exception as e:
    print("❌ Error:", e)
