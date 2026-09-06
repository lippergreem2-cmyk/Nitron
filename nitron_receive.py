#!/usr/bin/env python3

from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
INCOMING = ROOT / "Nitron-incoming"
PROJECT_FILE = ROOT / ".nitron_sync" / "project.json"


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(
            lambda: file.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def receive(package):
    package = Path(package)

    if not package.exists():
        raise FileNotFoundError(
            f"Package not found: {package}"
        )

    if not zipfile.is_zipfile(package):
        raise ValueError(
            "The selected file is not a valid ZIP package."
        )

    with zipfile.ZipFile(package, "r") as z:
        if "nitron-transfer.json" not in z.namelist():
            raise ValueError(
                "This is not a Nitron source-transfer package."
            )

        transfer = json.loads(
            z.read("nitron-transfer.json").decode("utf-8")
        )

    if transfer.get("name") != "Nitron":
        raise ValueError(
            "The package is not identified as Nitron."
        )

    if not PROJECT_FILE.exists():
        raise ValueError(
            "This Nitron copy has no project identity."
        )

    local_project = json.loads(
        PROJECT_FILE.read_text()
    )

    if transfer.get("project_id") != local_project.get("project_id"):
        raise ValueError(
            "The package belongs to a different Nitron project."
        )

    if INCOMING.exists():
        shutil.rmtree(INCOMING)

    INCOMING.mkdir(
        parents=True,
        exist_ok=True
    )

    with zipfile.ZipFile(package, "r") as z:
        print("Files in transfer package:", len(z.infolist()))
        print()

        for info in z.infolist():

            if info.is_dir():
                continue

            target = INCOMING / info.filename

            if not target.resolve().is_relative_to(
                INCOMING.resolve()
            ):
                raise ValueError(
                    "Unsafe path detected in transfer package."
                )

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            with z.open(info) as source:
                with target.open("wb") as destination:
                    shutil.copyfileobj(
                        source,
                        destination
                    )

    print()
    print("========================================")
    print(" Nitron Transfer Received")
    print("========================================")
    print()
    print("Project ID:")
    print(transfer["project_id"])
    print()
    print("Incoming copy:")
    print(INCOMING)
    print()
    print("The original Nitron project was NOT modified.")
    print()
    print("This is a staged copy. Nothing has been synchronized yet.")
    print()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python nitron_receive.py <Nitron-source-transfer.zip>"
        )
        raise SystemExit(1)

    receive(sys.argv[1])
