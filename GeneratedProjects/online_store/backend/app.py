from http.server import HTTPServer, SimpleHTTPRequestHandler


HOST = "127.0.0.1"
PORT = 8000


class NitronHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/api":

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                b'{"status":"online"}'
            )

            return

        return super().do_GET()


if __name__ == "__main__":

    server = HTTPServer(
        (HOST, PORT),
        NitronHandler
    )

    print(
        f"Server running at http://{HOST}:{PORT}"
    )

    server.serve_forever()
