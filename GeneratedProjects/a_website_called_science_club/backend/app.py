from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 8000

if __name__ == "__main__":
    server = HTTPServer(
        (HOST, PORT),
        SimpleHTTPRequestHandler,
    )

    print(
        f"Server running on http://{HOST}:{PORT}"
    )

    server.serve_forever()
