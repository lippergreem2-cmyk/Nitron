import os
import qrcode
from urllib.parse import quote, urlencode

QR_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "qr_codes"
)

os.makedirs(QR_DIR, exist_ok=True)


class NitronQR:
    """Universal QR-code generator for Nitron."""

    @staticmethod
    def generate(data, filename="nitron_qr.png",
                 error_correction="M", box_size=10, border=4):
        """Generate a QR code from ANY string/byte-compatible payload."""
        if data is None:
            raise ValueError("QR data cannot be empty")

        data = str(data)

        corrections = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }

        correction = corrections.get(
            str(error_correction).upper(),
            qrcode.constants.ERROR_CORRECT_M
        )

        if not filename.lower().endswith(".png"):
            filename += ".png"

        path = os.path.join(QR_DIR, filename)

        qr = qrcode.QRCode(
            version=None,
            error_correction=correction,
            box_size=box_size,
            border=border
        )

        qr.add_data(data)
        qr.make(fit=True)

        image = qr.make_image()
        image.save(path)

        return path

    @staticmethod
    def text(text):
        return NitronQR.generate(text, "text_qr.png")

    @staticmethod
    def url(url):
        return NitronQR.generate(url, "url_qr.png")

    @staticmethod
    def wifi(ssid, password="", security="WPA", hidden=False):
        def escape(value):
            return (
                str(value)
                .replace("\\", "\\\\")
                .replace(";", "\\;")
                .replace(",", "\\,")
                .replace(":", "\\:")
                .replace('"', '\\"')
            )

        security = security.upper()

        if security not in ("WPA", "WEP", "NOPASS"):
            security = "WPA"

        data = (
            f"WIFI:"
            f"T:{security};"
            f"S:{escape(ssid)};"
            f"P:{escape(password)};"
            f"H:{str(hidden).lower()};;"
        )

        return NitronQR.generate(data, "wifi_qr.png")

    @staticmethod
    def phone(number):
        return NitronQR.generate(
            f"tel:{number}",
            "phone_qr.png"
        )

    @staticmethod
    def sms(number, message=""):
        data = f"SMSTO:{number}:{message}"
        return NitronQR.generate(data, "sms_qr.png")

    @staticmethod
    def email(address, subject="", message=""):
        data = "mailto:" + str(address)

        params = {}

        if subject:
            params["subject"] = subject

        if message:
            params["body"] = message

        if params:
            data += "?" + urlencode(params)

        return NitronQR.generate(data, "email_qr.png")

    @staticmethod
    def contact(name, phone="", email="",
                organization="", website=""):
        data = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{name}\n"
            f"TEL:{phone}\n"
            f"EMAIL:{email}\n"
            f"ORG:{organization}\n"
            f"URL:{website}\n"
            "END:VCARD"
        )

        return NitronQR.generate(data, "contact_qr.png")

    @staticmethod
    def location(latitude, longitude):
        return NitronQR.generate(
            f"geo:{latitude},{longitude}",
            "location_qr.png"
        )

    @staticmethod
    def event(name, start, end=None, location="",
              description=""):
        data = (
            "BEGIN:VEVENT\n"
            f"SUMMARY:{name}\n"
            f"DTSTART:{start}\n"
        )

        if end:
            data += f"DTEND:{end}\n"

        if location:
            data += f"LOCATION:{location}\n"

        if description:
            data += f"DESCRIPTION:{description}\n"

        data += "END:VEVENT"

        return NitronQR.generate(data, "event_qr.png")

    @staticmethod
    def raw(data, filename="custom_qr.png",
            error_correction="H"):
        """
        Universal mode.

        Nitron can put arbitrary payloads into a QR code.
        This is the fallback for formats not built into the
        convenience methods above.
        """
        return NitronQR.generate(
            data,
            filename,
            error_correction=error_correction
        )


# Simple function aliases for the plugin system.

def generate(data, filename="nitron_qr.png", error_correction="M"):
    return NitronQR.generate(data, filename, error_correction)


def text(data):
    return NitronQR.text(data)


def url(data):
    return NitronQR.url(data)


def wifi(ssid, password="", security="WPA", hidden=False):
    return NitronQR.wifi(ssid, password, security, hidden)


def phone(number):
    return NitronQR.phone(number)


def sms(number, message=""):
    return NitronQR.sms(number, message)


def email(address, subject="", message=""):
    return NitronQR.email(address, subject, message)


def contact(name, phone="", email="", organization="", website=""):
    return NitronQR.contact(
        name, phone, email, organization, website
    )


def location(latitude, longitude):
    return NitronQR.location(latitude, longitude)


def event(name, start, end=None, location="", description=""):
    return NitronQR.event(
        name, start, end, location, description
    )


def raw(data, filename="custom_qr.png", error_correction="H"):
    return NitronQR.raw(data, filename, error_correction)


if __name__ == "__main__":
    path = raw(
        "Hello from Nitron - Universal QR Engine",
        "test_universal_qr.png"
    )

    print("Nitron Universal QR Engine")
    print("QR created:", path)


# ============================================================
# NITRON PLUGIN INTERFACE
# ============================================================

TRIGGERS = [
    "qr",
    "qr code",
    "qrcode",
    "generate qr",
    "generate a qr",
    "create qr",
    "create a qr",
    "make qr",
    "make a qr",
]


def matches(command):
    command = str(command).lower().strip()
    return any(trigger in command for trigger in TRIGGERS)


def run_command(command):
    command = str(command).strip()

    if not command:
        return (
            "What should I put into the QR code? "
            "Give me any text, URL, or custom data."
        )

    lowered = command.lower()

    prefixes = [
        "generate a qr code for",
        "generate qr code for",
        "generate a qr for",
        "generate qr for",
        "create a qr code for",
        "create qr code for",
        "create a qr for",
        "create qr for",
        "make a qr code for",
        "make qr code for",
        "make a qr for",
        "make qr for",
        "qr code for",
        "qr for",
        "qrcode for",
    ]

    data = ""

    for prefix in prefixes:
        if lowered.startswith(prefix):
            data = command[len(prefix):].strip()
            break

    if not data:
        data = command

        for trigger in TRIGGERS:
            if data.lower().startswith(trigger):
                data = data[len(trigger):].strip()
                break

    if not data:
        return (
            "Tell me what data the QR code should contain."
        )

    try:
        path = generate(data, filename=f"nitron_qr_{__import__("time").time_ns()}.png")

        return (
            f"[NITRON_IMAGE]{os.path.basename(path)}"
            f"[/NITRON_IMAGE]"
            f"Universal QR code created for: {data}"
        )

    except Exception as e:
        return f"I couldn't generate the QR code: {e}"


def plugin():
    return {
        "commands": TRIGGERS,
        "aliases": [
            "barcode",
            "generate qrcode",
            "create qrcode",
            "make qrcode"
        ],
        "run": run_command,
        "match_mode": "contains"
    }


# ============================================================
# PLUGIN TEST
# ============================================================

if __name__ == "__main__":
    result = run_command(
        "generate a QR code for Hello from Nitron"
    )

    print(result)
