from wait_for.parse import parse_uri, parse_address


def test_parse_uri():
    assert parse_uri("http://localhost:8080/path?query=1") == (
        "http",
        "localhost:8080",
        "/path?query=1",
    )
    assert parse_uri("file:///home/user/file.txt") == (
        "file",
        "",
        "/home/user/file.txt",
    )
    assert parse_uri("tcp://localhost:8080") == ("tcp", "localhost:8080", "")


def test_parse_address():
    assert parse_address("localhost:8080") == ("localhost", 8080, False)
    assert parse_address("[::1]:8080") == ("::1", 8080, True)
