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


def main():
    # sending logs

    log.debug("a")
    log.info("b")
    log.warning("c")

    try:
        1 / 0
    except Exception as e:
        log.exception(e)


if __name__ == "__main__":
    main()
