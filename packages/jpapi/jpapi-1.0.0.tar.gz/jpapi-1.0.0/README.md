# jpapi
Simple Python API Implementation using JSON, or "JSON Python API"

# Description
This is to make making python webservers for apis easy and quick. The objective is to enable
rapid development with little overhead.

# Installation
```bash
cd /usr/src
git clone https://github.com/eb3095/jpapi.git
cd jpapi/jpapi
python3 setup.py install
```

# Usage example
```python
import json

from jpapi import API, APIHandler, Endpoint

API_OBJ = None
FAILURE_TEMPLATE = {
    "error": {"code": 400, "message": "Invalid input"},
    "status": "fail",
}
RESPONSE_TEMPLATE = {"data": {"response": ""}, "status": "success"}


class GenericAPI(API):
    def __init__(self, config):
        super().__init__(config, "/v1", GenericAPIHandler)


class GenericAPIHandler(APIHandler):
    def init(self):
        GenericEndpoint(self)


class GenericEndpoint(Endpoint):
    def __init__(self, handler):
        self.path = "/generic/endpoint"
        self.required_fields = ["input", "another_value"]
        super().__init__(handler)

    def POST(self, data):
        inp = data["input"]
        # Do something
        result = "Hello!"
        return result, 200


def main():
    global API_OBJ
    with open("/etc/project/config.json") as f:
        config = json.load(f)
    API_OBJ = GenericAPI(config)
    API_OBJ.start()


if __name__ == "__main__":
    main()
```

The config is simple, and as you can see designed to work well with configs of the entire project.

```json
{
    "generic": {
        "program_key": "snip",
        "program_settings": 25,
        "another_program_setting": 52
    },
    "webserver": {
        "api_key": "snip",
        "host": "127.0.0.1",
        "port": 5000
    }
}
```