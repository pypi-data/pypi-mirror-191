from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


class APIHandler(BaseHTTPRequestHandler):
    endpoints = []
    api = None
    base = ""

    def __init__(self, api, base, request, client_address, server):
        self.api = api
        self.base = base
        self.init()
        super().__init__(request, client_address, server)

    def init(self):
        pass

    def do(self, action):
        if "Authorization" not in self.headers:
            self.return_result("Unauthorized", 401)
            return
        if self.headers["Authorization"] != f"Bearer {self.api.api_key}":
            self.return_result("Unauthorized", 401)
            return
        if action == "INVALID":
            self.return_result("Invalid action", 400)
            return
        data = None
        parsed = urlparse(self.path)
        path = parsed.path.replace(self.base, "")
        if action in ["GET", "DELETE"]:
            data = parse_qs(parsed.query)
        else:
            if (int(self.headers["Content-Length"])) < 1:
                self.return_result("Invalid usage, empty request", 400)
                return
            d_string = self.rfile.read(int(self.headers["Content-Length"]))
            try:
                data = json.loads(d_string)
            except Exception as e:
                self.return_result(f"Invalid JSON: {e}", 400)
                return
        for endpoint in self.endpoints:
            if path == endpoint.path:
                msg, code = endpoint._do(action, data)
                self.return_result(msg, code)
                return
        self.return_result("Endpoint not found", 404)

    def do_GET(self):
        self.do("GET")

    def do_DELETE(self):
        self.do("DELETE")

    def do_PUT(self):
        self.do("PUT")

    def do_POST(self):
        self.do("POST")

    def do_HEAD(self):
        self.do("INVALID")

    def do_CONNECT(self):
        self.do("INVALID")

    def do_OPTIONS(self):
        self.do("INVALID")

    def do_TRACE(self):
        self.do("INVALID")

    def return_result(self, msg, code):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        message = {"message": msg}
        self.wfile.write(bytes(json.dumps(message), "utf8"))


class API:
    api_key = None
    base = None
    _webserver = None

    def __init__(self, config, base, handler_class):
        self.api_key = config["webserver"]["api_key"]
        if base:
            self.base = base
        handler = lambda *args, **kwargs: handler_class(self, base, *args, **kwargs)
        self._webserver = HTTPServer(
            (config["webserver"]["host"], config["webserver"]["port"]), handler
        )

    def start(self):
        self._webserver.serve_forever()


class Endpoint:
    path = None
    required_fields = {"GET": [], "POST": [], "PUT": [], "DELETE": []}
    handler = None

    def __init__(self, handler):
        self.handler = handler
        self.handler.endpoints.append(self)

    def _do(self, action, data):
        for field in self.required_fields[action]:
            if field not in data:
                return f"Missing field: {field}", 400
        if action == "POST":
            return self._POST(data)
        elif action == "GET":
            return self._GET(data)
        elif action == "DELETE":
            return self._DELETE(data)
        elif action == "PUT":
            return self._PUT(data)

    def POST(self, data):
        return "Invalid action", 400

    def GET(self, data):
        return "Invalid action", 400

    def DELETE(self, data):
        return "Invalid action", 400

    def PUT(self, data):
        return "Invalid action", 400
