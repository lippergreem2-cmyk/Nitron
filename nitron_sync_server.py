#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import socket

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / ".nitron_sync"
MANIFEST_FILE = STATE_DIR / "manifest.json"
PROJECT_FILE = STATE_DIR / "project.json"
PORT = 8765


def load_json(path):
    return json.loads(path.read_text())


class NitronSyncHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(
            data,
            indent=2
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/nitron/info":

            project = load_json(PROJECT_FILE)
            manifest = load_json(MANIFEST_FILE)

            self.send_json({
                "name": "Nitron",
                "protocol_version": 1,
                "project_id": project["project_id"],
                "device_id": manifest["device_id"],
                "files": len(manifest["files"])
            })

            return

        if self.path == "/nitron/manifest":

            manifest = load_json(MANIFEST_FILE)

            self.send_json(manifest)

            return

        self.send_json(
            {
                "error": "Unknown Nitron endpoint."
            },
            404
        )

    def log_message(self, format, *args):
        print("[Nitron]", format % args)


def get_local_ip():
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        sock.close()


def main():

    if not PROJECT_FILE.exists():
        raise SystemExit(
            "Nitron project identity is missing."
        )

    if not MANIFEST_FILE.exists():
        raise SystemExit(
            "Nitron sync manifest is missing. "
            "Run: python nitron_sync.py"
        )

    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        NitronSyncHandler
    )

    project = load_json(PROJECT_FILE)
    manifest = load_json(MANIFEST_FILE)

    print()
    print("========================================")
    print(" Nitron Sync Server")
    print("========================================")
    print()
    print("Project ID:")
    print(project["project_id"])
    print()
    print("Device ID:")
    print(manifest["device_id"])
    print()
    print("Local address:")
    print(f"http://{get_local_ip()}:{PORT}")
    print()
    print("Endpoints:")
    print("  /nitron/info")
    print("  /nitron/manifest")
    print()
    print("Waiting for another Nitron copy...")
    print("Press Ctrl+C to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Nitron Sync Server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
