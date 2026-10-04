"""
wifi_qr.py
Generates a scannable QR code for a Wi-Fi network -- scanning it lets a
phone join the network without typing the password. Useful for sharing
your own network with guests.
"""

import wifi_qrcode_generator.generator as generator
from PIL import Image


def make_wifi_qr(ssid: str, password: str, security: str = "WPA", filename: str = "wifi_qr.png"):
    """
    security: "WPA" (most common), "WEP", or "nopass" for open networks.
    """
    qr = generator.wifi_qrcode(ssid, False, security, password)
    qr.make_image().save(filename)
    print(f"Saved QR code to {filename} -- scan it to join '{ssid}'.")


if __name__ == "__main__":
    ssid = input("Wi-Fi network name (SSID): ").strip()
    password = input("Wi-Fi password: ").strip()
    security = input("Security type (WPA/WEP/nopass) [default WPA]: ").strip() or "WPA"

    make_wifi_qr(ssid, password, security)
