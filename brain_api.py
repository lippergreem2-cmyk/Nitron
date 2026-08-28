# ~/Nitron/brain_api.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import traceback

from brain import ask


class NitronBrainServer(BaseHTTPRequestHandler):

    def send_json(self, data):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode()
        )


    def do_GET(self):

        response = {
            "status": "online",
            "name": "Nitron Brain Server",
            "message": "Brain system ready"
        }

        self.send_json(response)



    def do_POST(self):

        try:

            length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(length)

            data = json.loads(body)


            command = data.get(
                "command",
                ""
            )


            if command == "":

                self.send_json({
                    "error": "No command received"
                })

                return



            answer = ask(command)



            response = {

                "command": command,

                "answer": answer

            }


            self.send_json(response)



        except Exception as e:


            print("ERROR:")
            traceback.print_exc()


            self.send_json({

                "error": str(e)

            })



server = HTTPServer(
    ("0.0.0.0", 8081),
    NitronBrainServer
)


print(
    "Nitron Brain Server online on port 8081"
)


server.serve_forever()
