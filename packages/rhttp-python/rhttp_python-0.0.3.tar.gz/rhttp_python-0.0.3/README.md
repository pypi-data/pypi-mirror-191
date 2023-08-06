# RHTTP-python
Python interface for RHTTP server

## Installation
Install the latest version of `rhttp-python` with running installation command:
```shell
pip install rhttp-python
```

## Usage
First you need to import required packages:
```python
# RHTTP server
from rhttp_python import RHTTPServer
# Asyncio library for running server
import asyncio
```

First you need to create server by passing redis host and port:

```python
server = RHTTPServer("127.0.0.1", 6379)
```

Then you can define endpoints using `route` decorator

```python
@server.route("/", "GET")
def home(req, res):
    print(req)
    return res.status(200).content_type("text/html").send("<h1>test</h1>")
```

First parameter of decorator is "path" of endpoint and second is http method

At the end you need run server:
```python
asyncio.run(server.listen())
```



## License
This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.