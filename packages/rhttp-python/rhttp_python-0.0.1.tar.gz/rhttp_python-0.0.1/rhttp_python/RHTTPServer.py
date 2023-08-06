import asyncio
import redis.asyncio as redis
import re


def parse_http_message(message: str):
    parsed = message.split("\r\n\r\n")
    header_lines = parsed[0].split("\r\n")
    body = parsed[1] if len(parsed) > 1 else ""

    # Parse the request line or status line
    match = re.match(r"(?P<version>HTTP/\d\.\d) (?P<status>\d{3}) (?P<message>.+)$", header_lines[0])
    if match:
        return {
            "status": int(match.group("status")),
            "message": match.group("message"),
            "headers": parse_headers(header_lines[1:]),
            "body": body
        }
    else:
        # Parse the request line
        method, path, query = parse_request_line(header_lines[0])
        return {
            "method": method,
            "path": path,
            "query": query,
            "headers": parse_headers(header_lines[1:]),
            "body": body
        }


def parse_request_line(request_line: str):
    match = re.match(r"(?P<method>\w+) (?P<path>[^\s\?]+)(\?(?P<query>.+))?\sHTTP/\d\.\d", request_line)
    return match.group("method"), match.group("path"), match.group("query")


def parse_headers(header_lines):
    headers = {}
    for line in header_lines:
        key, value = line.split(": ")
        headers[key] = value
    return headers


def serialize_http_message(message):
    if "status" in message:
        # Serialize a response
        status_line = f"HTTP/1.1 {message['status']} {message['message']}\r\n"
    else:
        # Serialize a request
        status_line = f"{message['method']} {message['path']}"
        if message["query"]:
            status_line += f"?{message['query']}"
        status_line += " HTTP/1.1\r\n"

    headers = "".join([f"{key}: {value}\r\n" for key, value in message["headers"].items()])
    body = message["body"]
    return f"{status_line}{headers}\r\n{body}"


def random_name():
    import random
    return "".join(
        [random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(0, 20)])


def http_status_code_to_message(status_code):
    messages = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported"
    }
    return messages.get(status_code, "Unknown")


class Response:
    def __init__(self, req):
        self.request = req
        self.content_type_ = "plain/text"
        self.body = ""
        self.status_code = 200
        self.message = http_status_code_to_message(self.status_code)

    def status(self, code: int):
        self.status_code = code
        self.message = http_status_code_to_message(self.status_code)
        return self

    def content_type(self, content_type: str):
        self.content_type_ = content_type
        return self

    def send(self, body: str) -> str:
        self.body = body
        return serialize_http_message({
            "message": self.message,
            "status": self.status_code,
            "headers": {
                "Content-Type": self.content_type_,
                "Content-Length": len(self.body),
                "X-Socket-ID": self.request["headers"]["X-Socket-ID"],
            },
            "body": self.body,
        })


async def reader(channel: redis.client.PubSub, redis_context: redis.Redis, name: str, desc: str, endpoints):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None and message['type'] == "message":
            if message["channel"].decode('utf-8') == "HEARTBEAT":
                await redis_context.publish("ACKNOWLEDGE_PIPE", f"{name}{chr(14)}{desc}")
            elif message["channel"].decode('utf-8') == "REQUEST_PIPE":
                data = message['data'].decode('utf-8')
                req = parse_http_message(data)

                found = False
                for ep in endpoints:
                    if ep["path"] == req["path"] and ep["method"] == req["method"]:
                        res = ep["callback"](req, Response(req))
                        await redis_context.publish("RESPONSE_PIPE", res)
                        found = True
                        break
                if not found:
                    await redis_context.publish("REJECT_PIPE", req["headers"]["X-Socket-ID"])


class RHTTPServer:
    def __init__(self, host: str, port: int, name: str = random_name(), desc: str = "PYTHON"):
        self.host, self.port = host, port
        self.name, self.desc = name, desc
        self.endpoints = []

    def __add_ep(self, path, method, callback):
        method = method.upper()
        self.endpoints.append({
            "path": path,
            "method": method,
            "callback": callback,
        })

    def route(self, path, method):
        def route_func(func):
            self.__add_ep(path, method, func)
            return func

        return route_func

    def get(self, path, callback):
        self.__add_ep(path, "GET", callback)

    def post(self, path, callback):
        self.__add_ep(path, "POST", callback)

    def put(self, path, callback):
        self.__add_ep(path, "PUT", callback)

    def patch(self, path, callback):
        self.__add_ep(path, "PATCH", callback)

    def delete(self, path, callback):
        self.__add_ep(path, "DELETE", callback)

    def head(self, path, callback):
        self.__add_ep(path, "HEAD", callback)

    def options(self, path, callback):
        self.__add_ep(path, "OPTIONS", callback)

    def connect(self, path, callback):
        self.__add_ep(path, "CONNECT", callback)

    def trace(self, path, callback):
        self.__add_ep(path, "TRACE", callback)

    async def listen(self):
        print("Server is listening to Redis")
        r = await redis.from_url(f"redis://{self.host}:{self.port}")
        self.redis_context = r
        async with self.redis_context.pubsub() as pubsub:
            await pubsub.subscribe("REQUEST_PIPE", "HEARTBEAT")
            future = asyncio.create_task(reader(pubsub, self.redis_context, self.name, self.desc, self.endpoints))
            await future
