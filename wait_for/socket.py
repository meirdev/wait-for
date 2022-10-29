import socket


def _socket_base(
    type_: socket.SocketKind,
    /,
    family: socket.AddressFamily,
    address: tuple[str, int] | str,
    timeout: float | None,
) -> bool:
    try:
        with socket.socket(family, type_) as sock:
            sock.settimeout(timeout)
            sock.connect(address)
    except socket.error:
        return False

    return True


def tcp(**kwargs) -> bool:
    return _socket_base(socket.SOCK_STREAM, **kwargs)


def udp(**kwargs) -> bool:
    return _socket_base(socket.SOCK_DGRAM, **kwargs)
