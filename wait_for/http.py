import socket
from http.client import HTTPConnection, HTTPException, HTTPSConnection
from typing import Callable, Type

ValidateStatus = Callable[[int], bool]


def _http_base(
    cls: Type[HTTPConnection],
    /,
    address: str,
    url: str,
    method: str,
    timeout: float | None,
    validate_status: ValidateStatus,
) -> bool:
    connection = cls(address, timeout=timeout)

    try:
        connection.request(method, url)
        response = connection.getresponse()

        return validate_status(response.status)
    except (socket.error, HTTPException) as e:
        return False
    finally:
        connection.close()


def http(**kwargs) -> bool:
    return _http_base(HTTPConnection, **kwargs)


def https(**kwargs) -> bool:
    return _http_base(HTTPSConnection, **kwargs)
