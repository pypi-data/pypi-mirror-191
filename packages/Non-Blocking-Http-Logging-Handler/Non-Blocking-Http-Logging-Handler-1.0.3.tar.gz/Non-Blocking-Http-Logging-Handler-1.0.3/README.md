# Non-Blocking-Http-Logging-Handler


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)

This library provides a non-blocking http logging handler for python 3.8+ that can be used to send logs to a logging 
service in a non-blocking way via http requests in a very simple way.

## Installation

```bash
pip install non-blocking-http-logging-handler
```

## Basic Usage

```python
import logging

from non_blocking_http_handler.handler import NonBlockingHttpHandler

httpHandler = NonBlockingHttpHandler(
    url='http://localhost:5000/logs',
    max_workers=10,
    max_retries=3
)

log = logging.getLogger()
log.setLevel(logging.DEBUG)  # set level to DEBUG to see all logs
log.addHandler(httpHandler)
```

The complete example is available in the examples folder in the file `basic_usage.py`.

### Parameters explanation

- `url`: The url of the logging service.
- `max_workers`: The maximum number of workers that will be used to send logs to the logging service.
- `max_retries`: The maximum number of retries that will be done if the request fails.
- `extra`: A dictionary with extra fields that will be added to the log (explained below).

### Output format

The output format of the logs is a json with the following fields:
- `level`: The level of the log.
- `message`: The message of the log.
- `file`: The file name of the log.
- `line`: The line number of the log.
- `timestamp`: The timestamp of the log.
- the extra fields that you may have added to the log.

for example:

```json
{
    "level": "INFO",
    "message": "This is a log",
    "file": "basic_usage.py",
    "line": 10,
    "timestamp": "2021-10-10 10:10:10"
}
```

## Add extra fields to the log

In same cases you may want to add extra fields to the log, for example, 
if you are using a logging handler to send logs to a logging service, 
you may want to add the service name to the log or the ip.

For this purpose, you can use the `extra` parameter of the `NonBlockingHttpHandler` class.

```python
import logging
import socket  # for get hostname amd ip

from non_blocking_http_handler.handler import NonBlockingHttpHandler

httpHandler = NonBlockingHttpHandler(
    url='http://localhost:5000/logs',
    max_workers=5,
    max_retries=3,
    extra={
        'hostname': socket.gethostname()
    }
)

log = logging.getLogger()
log.setLevel(logging.DEBUG)  # set level to DEBUG to see all logs
log.addHandler(httpHandler)
```

The complete example is available in the examples folder in the file `extra_fields.py`.



