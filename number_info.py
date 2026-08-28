import phonenumbers
from phonenumbers import geocoder, carrier, timezone

GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

print(GREEN + """
╔══════════════════════════════════════╗
║       ADVANCED NUMBER INFO           ║
╠══════════════════════════════════════╣
║     PUBLIC NUMBERING DATA ONLY       ║
╚══════════════════════════════════════╝
""" + RESET)

number = input("Enter phone number (+country code): ").strip()

try:
    phone = phonenumbers.parse(number, None)

    valid = phonenumbers.is_valid_number(phone)
    possible = phonenumbers.is_possible_number(phone)

    print(CYAN + "\n========== RESULT ==========" + RESET)

    print("📱 Number:     ",
          phonenumbers.format_number(
              phone,
              phonenumbers.PhoneNumberFormat.INTERNATIONAL
          ))

    print("🌍 Country:    ",
          geocoder.description_for_number(phone, "en") or "Unknown")

    print("🗺️ Region:     ",
          geocoder.description_for_number(phone, "en") or "Not available")

    print("🏙️ County:     Not reliably available")

    print("📡 Carrier:    ",
          carrier.name_for_number(phone, "en") or "Unknown")

    zones = timezone.time_zones_for_number(phone)
    print("🕐 Timezone:   ",
          ", ".join(zones) if zones else "Unknown")

    print("🔢 Country code:", "+" + str(phone.country_code))
    print("✅ Possible:   ", possible)
    print("✅ Valid:      ", valid)

    print(CYAN + "\n============================" + RESET)
    print("ℹ️ No live GPS location is available from this lookup.")

except phonenumbers.NumberParseException as e:
    print("\n❌ Invalid phone number.")
    print("Use international format, e.g. +254...")
