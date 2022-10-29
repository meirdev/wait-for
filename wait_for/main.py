import enum
import dataclasses
import socket
import threading
import time
from functools import partial
from typing import Callable

from .file import file
from .http import ValidateStatus, http, https
from .parse import parse_address, parse_uri
from .process import Process
from .socket import tcp, udp


@dataclasses.dataclass
class HTTPOptions:
    method: str
    timeout: float | None
    validate_status: ValidateStatus


@dataclasses.dataclass
class SocketOptions:
    timeout: float | None


@dataclasses.dataclass
class Options:
    http: HTTPOptions = HTTPOptions("GET", None, lambda status: 200 <= status < 300)
    socket: SocketOptions = SocketOptions(None)


class Scheme(str, enum.Enum):
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    HTTPS = "https"
    FILE = "file"


def _loop(fn: Callable[[], bool], delay: float, reverse: bool, interval: float) -> None:
    if delay:
        time.sleep(delay)

    while True:
        if fn() is not reverse:
            return

        if interval:
            time.sleep(interval)


def _run(fn: Callable[[], None], timeout: float | None) -> bool:
    loop_process = Process(target=fn)
    loop_process.start()

    if timeout:
        timer = threading.Timer(timeout, loop_process.terminate)
        timer.start()
    else:
        timer = None

    loop_process.join()

    if timer:
        timer.cancel()

    return loop_process.exit_code == 0


def wait_for(
    uri: str,
    delay: float = 0.0,
    interval: float = 0.25,
    timeout: float | None = None,
    reverse: bool = False,
    options: Options | None = None,
) -> bool:
    if options is None:
        options = Options()

    uri_parse = parse_uri(uri)

    scheme = uri_parse.scheme.lower()
    address = uri_parse.address
    path = uri_parse.path

    if not address and not path:
        raise ValueError("the address and path cannot be empty together")

    if scheme == Scheme.TCP or scheme == Scheme.UDP:
        if address and path:
            raise ValueError("address and path cannot be used together in tcp/udp")

        address_: tuple[str, int] | str

        if address:
            address_parse = parse_address(address)

            address_ = address_parse.host, address_parse.port
            family = socket.AF_INET6 if address_parse.is_ip_v6 else socket.AF_INET
        else:
            address_ = path
            family = socket.AF_UNIX

        fn = partial(
            tcp if scheme == Scheme.TCP else udp,
            family=family,
            address=address_,
            timeout=options.socket.timeout,
        )

    elif scheme == Scheme.HTTP or scheme == Scheme.HTTPS:
        fn = partial(
            http if scheme == Scheme.HTTP else https,
            address=address,
            url=path,
            method=options.http.method,
            timeout=options.http.timeout,
            validate_status=options.http.validate_status,
        )

    elif scheme == Scheme.FILE:
        if address:
            path_ = f"/{address}{path}"
        else:
            path_ = path

        fn = partial(file, path=path_)

    else:
        raise ValueError(f"unknown scheme: {scheme!r}")

    run_fn = partial(_loop, fn=fn, delay=delay, reverse=reverse, interval=interval)

    return _run(run_fn, timeout)
