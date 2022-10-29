import urllib.parse
from typing import NamedTuple


class ParseURIResult(NamedTuple):
    scheme: str
    address: str
    path: str


class ParseAddressResult(NamedTuple):
    host: str
    port: int
    is_ip_v6: bool


def parse_uri(uri: str) -> ParseURIResult:
    url_split = urllib.parse.urlsplit(uri, allow_fragments=False)

    scheme, address, path = url_split.scheme, url_split.netloc, url_split.path

    if url_split.query:
        path = f"{path}?{url_split.query}"

    return ParseURIResult(scheme, address, path)


def parse_address(address: str) -> ParseAddressResult:
    is_ip_v6 = False

    address_split = address.rsplit(":", maxsplit=1)
    if len(address_split) != 2:
        raise ValueError("address must be in the format host:port")

    host, port = address_split

    if host[0] == "[" and host[-1] == "]":
        host = host[1:-1]
        is_ip_v6 = True

    port = int(port)

    return ParseAddressResult(host, port, is_ip_v6)
