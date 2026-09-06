#!/usr/bin/env python3

import hashlib
import json
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".nitron_sync"
LOCAL_MANIFEST = STATE_DIR / "manifest.json"
PROJECT_FILE = STATE_DIR / "project.json"

EXCLUDED_PARTS = {
    ".git",
    ".gradle",
    ".idea",
    "build",
    "__pycache__",
    ".nitron_sync",
}

EXCLUDED_NAMES = {
    ".env",
    "config.env",
    "google-services.json",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def should_skip(path):
    relative = path.relative_to(ROOT)

    if any(part in EXCLUDED_PARTS for part in relative.parts):
        return True

    if path.name in EXCLUDED_NAMES:
        return True

    if path.name.endswith(".jks"):
        return True

    if path.name.endswith(".keystore"):
        return True

    if path.name.endswith(".p12"):
        return True

    if path.name.endswith(".pfx"):
        return True

    return False


def build_local_manifest():
    files = {}

    for path in ROOT.rglob("*"):

        if not path.is_file():
            continue

        if should_skip(path):
            continue

        relative = path.relative_to(ROOT).as_posix()

        try:
            files[relative] = sha256_file(path)
        except OSError:
            pass

    return files


def fetch_json(url):
    print()
    print("Connecting to:")
    print(url)

    with urllib.request.urlopen(
        url,
        timeout=10
    ) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


def compare_manifests(local, remote):
    local_files = local["files"]
    remote_files = remote["files"]

    added = sorted(
        set(remote_files) - set(local_files)
    )

    removed = sorted(
        set(local_files) - set(remote_files)
    )

    changed = sorted(
        path
        for path in set(local_files) & set(remote_files)
        if local_files[path] != remote_files[path]
    )

    unchanged = sorted(
        path
        for path in set(local_files) & set(remote_files)
        if local_files[path] == remote_files[path]
    )

    return added, removed, changed, unchanged


def main():

    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print("  python nitron_sync_client.py <server-ip>")
        print()
        print("Example:")
        print("  python nitron_sync_client.py 192.168.1.114")
        return 1

    server_ip = sys.argv[1]

    if not PROJECT_FILE.exists():
        print("ERROR: Nitron project identity is missing.")
        return 1

    if not LOCAL_MANIFEST.exists():
        print("ERROR: Local manifest is missing.")
        print("Run: python nitron_sync.py")
        return 1

    local_project = load_json(PROJECT_FILE)
    local_manifest = load_json(LOCAL_MANIFEST)

    base_url = f"http://{server_ip}:8765"

    try:
        remote_info = fetch_json(
            f"{base_url}/nitron/info"
        )

        remote_manifest = fetch_json(
            f"{base_url}/nitron/manifest"
        )

    except Exception as e:
        print()
        print("ERROR: Could not connect to Nitron.")
        print(e)
        return 1

    print()
    print("========================================")
    print(" Nitron Sync Preview")
    print("========================================")

    print()
    print("Local project ID:")
    print(local_project["project_id"])

    print()
    print("Remote project ID:")
    print(remote_info["project_id"])

    if local_project["project_id"] != remote_info["project_id"]:
        print()
        print("ERROR: These are different Nitron projects.")
        print("Sync cancelled.")
        return 1

    if local_manifest["device_id"] == remote_info["device_id"]:
        print()
        print("ERROR: Local and remote device IDs are identical.")
        print("This appears to be the same Nitron device.")
        print("Sync cancelled.")
        return 1

    print()
    print("Remote device ID:")
    print(remote_info["device_id"])

    print()
    print("Local files:", len(local_manifest["files"]))
    print("Remote files:", len(remote_manifest["files"]))

    added, removed, changed, unchanged = compare_manifests(
        local_manifest,
        remote_manifest
    )

    print()
    print("---------------")
    print("SYNC PREVIEW")
    print("---------------")

    print()
    print("Remote-only files:", len(added))
    print("Local-only files:", len(removed))
    print("Changed files:", len(changed))
    print("Unchanged files:", len(unchanged))

    if added:
        print()
        print("REMOTE → LOCAL")
        for path in added[:50]:
            print("  +", path)

        if len(added) > 50:
            print(
                f"  ... and {len(added) - 50} more"
            )

    if removed:
        print()
        print("LOCAL → REMOTE")
        for path in removed[:50]:
            print("  -", path)

        if len(removed) > 50:
            print(
                f"  ... and {len(removed) - 50} more"
            )

    if changed:
        print()
        print("CHANGED ON BOTH / DIFFERENT CONTENT")
        for path in changed[:50]:
            print("  *", path)

        if len(changed) > 50:
            print(
                f"  ... and {len(changed) - 50} more"
            )

    print()
    print("No files were modified.")
    print("This was a preview only.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
