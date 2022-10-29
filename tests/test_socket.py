import socket
from unittest.mock import patch

from wait_for.socket import tcp, udp


@patch("socket.socket.connect")
def test_tcp(mock_socket):
    assert tcp(family=socket.AF_INET, address=("localhost", 8080), timeout=10)


@patch("socket.socket.connect")
def test_udp(mock_socket):
    assert udp(family=socket.AF_INET, address=("localhost", 8080), timeout=10)


@patch("socket.socket.connect")
def test_socket_failed(mock_socket):
    mock_socket.side_effect = socket.error("error")

    assert tcp(family=socket.AF_INET, address=("localhost", 8080), timeout=10) is False
