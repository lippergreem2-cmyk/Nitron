#!/usr/bin/env python3

from pathlib import Path
import zipfile
import json
import hashlib
import time

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Nitron-source-transfer.zip"

EXCLUDE_DIRS = {
    ".git",
    ".gradle",
    "build",
    "__pycache__",
    ".idea",
}

EXCLUDE_FILES = {
    OUTPUT.name,
}

def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def should_include(path):
    relative = path.relative_to(ROOT)

    if path.name in EXCLUDE_FILES:
        return False

    if any(part in EXCLUDE_DIRS for part in relative.parts):
        return False

    return path.is_file()


def build_package():

    files = [
        path
        for path in ROOT.rglob("*")
        if should_include(path)
    ]

    manifest = {
        "name": "Nitron",
        "type": "source_transfer",
        "protocol_version": 1,
        "created_at": int(time.time()),
        "file_count": len(files),
        "files": []
    }

    for path in files:

        relative = path.relative_to(ROOT)

        manifest["files"].append({
            "path": str(relative),
            "size": path.stat().st_size,
            "sha256": sha256(path)
        })

    with zipfile.ZipFile(
        OUTPUT,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        archive.writestr(
            "nitron-transfer.json",
            json.dumps(
                manifest,
                indent=2
            )
        )

        for path in files:

            relative = path.relative_to(ROOT)

            archive.write(
                path,
                str(relative)
            )

    print()
    print("========================================")
    print(" Nitron source transfer package created")
    print("========================================")
    print()
    print(f"Files: {len(files)}")
    print(f"Package: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size:,} bytes")
    print()
    print("This package contains Nitron's source tree.")
    print()


if __name__ == "__main__":
    build_package()
