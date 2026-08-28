import os
import requests

API = "https://api.github.com/repos/lippergreem2-cmyk/Nitron/releases/latest"
OUT = os.path.expanduser("~/storage/downloads/Nitron-latest-signed.apk")

print("Checking latest Nitron release...")

r = requests.get(API, timeout=30)
r.raise_for_status()

release = r.json()

print("Latest release:", release.get("tag_name"))

apk = None

for asset in release.get("assets", []):
    if asset["name"].lower().endswith(".apk"):
        apk = asset
        break

if apk is None:
    raise RuntimeError("No APK found in the latest release.")

print("APK:", apk["name"])
print("Downloading...")

with requests.get(apk["browser_download_url"], stream=True, timeout=60) as r:
    r.raise_for_status()

    with open(OUT, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

print("Download complete.")
print("Saved:", OUT)
