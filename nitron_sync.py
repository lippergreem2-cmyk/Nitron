#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import shutil
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".nitron_sync"
MANIFEST_FILE = STATE_DIR / "manifest.json"
DEVICE_FILE = STATE_DIR / "device.json"

EXCLUDED_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    "__pycache__",
    "build",
    ".nitron_sync",
}

EXCLUDED_FILES = {
    "Nitron-source-transfer.zip",
    "Nitron-transfer.zip",
    ".env",
    "config.env",
    "google-services.json",
    "nitron-release.jks",
}

def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()

def should_include(path):
    relative = path.relative_to(ROOT)

    if path.name in EXCLUDED_FILES:
        return False

    if any(
        part in EXCLUDED_DIRS
        for part in relative.parts
    ):
        return False

    if path.suffix.lower() in {
        ".jks",
        ".keystore",
        ".p12",
        ".pfx",
    }:
        return False

    return path.is_file()

def ensure_state():
    STATE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

def get_device_id():
    ensure_state()

    if DEVICE_FILE.exists():
        data = json.loads(
            DEVICE_FILE.read_text()
        )
        return data["device_id"]

    device_id = str(uuid.uuid4())

    DEVICE_FILE.write_text(
        json.dumps(
            {
                "device_id": device_id,
                "created_at": int(time.time())
            },
            indent=2
        )
    )

    return device_id

def get_project_id():
    project_file = STATE_DIR / "project.json"

    if not project_file.exists():
        raise RuntimeError(
            "Nitron project identity is missing."
        )

    data = json.loads(
        project_file.read_text()
    )

    if not data.get("project_id"):
        raise RuntimeError(
            "Nitron project ID is missing."
        )

    return data["project_id"]

def build_manifest():
    ensure_state()

    files = {}

    for path in ROOT.rglob("*"):
        if not should_include(path):
            continue

        relative = str(
            path.relative_to(ROOT)
        )

        files[relative] = {
            "size": path.stat().st_size,
            "sha256": sha256(path)
        }

    manifest = {
        "name": "Nitron",
        "protocol_version": 1,
        "project_id": get_project_id(),
        "device_id": get_device_id(),
        "generated_at": int(time.time()),
        "files": files
    }

    MANIFEST_FILE.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True
        )
    )

    return manifest

def compare_manifests(local, remote):
    local_files = local.get("files", {})
    remote_files = remote.get("files", {})

    local_paths = set(local_files)
    remote_paths = set(remote_files)

    return {
        "added": sorted(remote_paths - local_paths),
        "deleted": sorted(local_paths - remote_paths),
        "modified": sorted(
            path
            for path in local_paths & remote_paths
            if local_files[path]["sha256"]
            != remote_files[path]["sha256"]
        ),
        "unchanged": sorted(
            path
            for path in local_paths & remote_paths
            if local_files[path]["sha256"]
            == remote_files[path]["sha256"]
        ),
    }

def compare_with_manifest(path):
    local = build_manifest()

    remote_path = Path(path)

    if not remote_path.exists():
        raise FileNotFoundError(
            f"Manifest not found: {remote_path}"
        )

    remote = json.loads(
        remote_path.read_text()
    )

    if remote.get("name") != "Nitron":
        raise ValueError(
            "The selected manifest is not a Nitron manifest."
        )

    if remote.get("project_id") != local.get("project_id"):
        raise ValueError(
            "The two Nitron copies belong to different projects."
        )

    if remote.get("device_id") == local.get("device_id"):
        raise ValueError(
            "The selected manifest belongs to this Nitron copy."
        )

    result = compare_manifests(local, remote)

    print()
    print("========================================")
    print(" Nitron Sync Preview")
    print("========================================")
    print()
    print("New on remote: ", len(result["added"]))
    print("Modified:      ", len(result["modified"]))
    print("Deleted:       ", len(result["deleted"]))
    print("Unchanged:     ", len(result["unchanged"]))
    print()
    print("DRY RUN: no files were changed.")
    print()

    return result

if __name__ == "__main__":

    if len(sys.argv) == 1:
        manifest = build_manifest()

        print()
        print("========================================")
        print(" Nitron Sync Manifest")
        print("========================================")
        print()
        print("Project ID:")
        print(manifest["project_id"])
        print()
        print("Device ID:")
        print(manifest["device_id"])
        print()
        print("Tracked files:")
        print(len(manifest["files"]))
        print()
        print("Manifest:")
        print(MANIFEST_FILE)
        print()

    elif sys.argv[1] == "compare":

        if len(sys.argv) != 3:
            print(
                "Usage: python nitron_sync.py compare <manifest.json>"
            )
            raise SystemExit(1)

        compare_with_manifest(sys.argv[2])

    else:
        print("Usage:")
        print("  python nitron_sync.py")
        print("  python nitron_sync.py compare <manifest.json>")
