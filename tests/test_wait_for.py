from unittest.mock import patch

import pytest

from wait_for import wait_for


@patch("wait_for.main._run")
def test_wait_for_file(mock_run):
    mock_run.return_value = True

    assert wait_for("file:///home/dir/file.txt")
    assert wait_for("file://localhost/home/dir/file.txt")


@patch("wait_for.main._run")
def test_wait_for_socket(mock_run):
    mock_run.return_value = True

    assert wait_for("tcp://127.0.0.1:8080")
    assert wait_for("udp://[::1]:9000")
    assert wait_for("tcp:///tmp/socket.sock")


def test_wait_for_socket_host_without_port_error():
    with pytest.raises(ValueError) as e:
        wait_for("tcp://127.0.0.1")

    assert "address must be in the format host:port" in str(e.value)


def test_wait_for_socket_address_with_path_error():
    with pytest.raises(ValueError) as e:
        wait_for("udp://127.0.0.1:9000/file.txt")

    assert "address and path cannot be used together in tcp/udp" in str(e.value)


@patch("wait_for.main._run")
def test_wait_for_http(mock_run):
    mock_run.return_value = True

    assert wait_for("http://127.0.0.1:8080/file.txt")


def test_wait_for_unknown_error():
    with pytest.raises(ValueError) as e:
        assert wait_for("ftp://127.0.0.1:8080/file.txt")

    assert "unknown scheme: 'ftp'" in str(e.value)


def test_wait_for_address_and_path_empty_error():
    with pytest.raises(ValueError) as e:
        assert wait_for("udp://")

    assert "the address and path cannot be empty together" in str(e.value)
