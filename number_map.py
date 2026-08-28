import phonenumbers
import webbrowser
from phonenumbers import geocoder, carrier, timezone
from geopy.geocoders import Nominatim

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

print(GREEN + """
╔══════════════════════════════════════╗
║       NITRON NUMBER MAP              ║
╠══════════════════════════════════════╣
║       PUBLIC LOCATION LOOKUP         ║
╚══════════════════════════════════════╝
""" + RESET)

number = input("📱 Enter phone number: ").strip()

try:
    phone = phonenumbers.parse(number, None)

    if not phonenumbers.is_valid_number(phone):
        print("\n❌ Number is not valid.")
        raise SystemExit

    region = geocoder.description_for_number(phone, "en")
    carrier_name = carrier.name_for_number(phone, "en")
    zones = timezone.time_zones_for_number(phone)

    print(CYAN + "\n========== NUMBER ==========" + RESET)

    print("📱 Number:   ",
          phonenumbers.format_number(
              phone,
              phonenumbers.PhoneNumberFormat.INTERNATIONAL
          ))

    print("🌍 Region:   ", region or "Unknown")
    print("📡 Carrier:  ", carrier_name or "Unknown")
    print("🕐 Timezone: ", ", ".join(zones) if zones else "Unknown")

    # Convert the public region description into map coordinates
    geolocator = Nominatim(
        user_agent="nitron-number-map"
    )

    location = geolocator.geocode(region)

    if location:
        latitude = location.latitude
        longitude = location.longitude

        print("📍 Map area: ", location.address)
        print("🌐 Latitude: ", latitude)
        print("🌐 Longitude:", longitude)

        # Open OpenStreetMap
        map_url = (
            "https://www.openstreetmap.org/"
            f"?mlat={latitude}&mlon={longitude}"
            f"#map=6/{latitude}/{longitude}"
        )

        print("\n🗺️ Opening map...")
        webbrowser.open(map_url)

    else:
        print("\n⚠️ Could not find map coordinates for the region.")

    print(GREEN + "\n============================" + RESET)
    print("ℹ️ The map shows the public region,")
    print("   not the phone's live GPS position.")

except phonenumbers.NumberParseException:
    print("\n❌ Could not understand the phone number.")
    print("Use international format, e.g. +254...")
