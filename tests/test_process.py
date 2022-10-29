from unittest.mock import patch

import pytest

from wait_for.process import Process


@patch("os.kill")
@patch("os.waitpid")
@patch("os.fork")
@patch("sys.exit")
def test_process(mock_exit, mock_fork, mock_waitpid, mock_kill, capsys):
    mock_exit.return_value = 0
    mock_fork.return_value = 0
    mock_waitpid.return_value = (0, 0)

    def fn():
        print("Hello")

    process = Process(target=fn)

    process.start()

    captured = capsys.readouterr()
    assert captured.out == "Hello\n"

    mock_fork.assert_called_once()
    mock_exit.assert_called_once_with(0)

    process.terminate()
    process.join()

    mock_waitpid.assert_called_once_with(0, 0)

    assert process.exit_code == 0


def test_process_join_error():
    process = Process(target=lambda: None)

    with pytest.raises(RuntimeError):
        process.join()


def test_process_terminate_error():
    process = Process(target=lambda: None)

    with pytest.raises(RuntimeError):
        process.terminate()
