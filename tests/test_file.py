import tempfile

from wait_for.file import file


def test_file():
    with tempfile.NamedTemporaryFile() as f:
        assert file(f.name)

    assert file(f.name) is False
