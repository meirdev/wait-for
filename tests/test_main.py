import threading
import time
from unittest.mock import Mock, PropertyMock, patch

from wait_for.main import _run, _loop


@patch("wait_for.main.Process.exit_code", new_callable=PropertyMock)
@patch("wait_for.main.Process.terminate")
@patch("wait_for.main.Process.join")
@patch("wait_for.main.Process.start")
def test_run(mock_start, mock_join, mock_terminate, mock_exit_code):
    e = threading.Event()
    e.clear()

    mock_exit_code.return_value = 0
    mock_join.side_effect = lambda: time.sleep(3.0)
    mock_terminate.side_effect = lambda: e.set()

    def fn():
        def inner():
            e.wait()

        t = threading.Thread(target=inner)
        t.start()

    mock_start.side_effect = fn

    assert _run(lambda: None, 2.0)

    assert mock_terminate.called


@patch("wait_for.main.Process.exit_code", new_callable=PropertyMock)
@patch("wait_for.main.Process.terminate")
@patch("wait_for.main.Process.join")
@patch("wait_for.main.Process.start")
def test_run_no_timeout(mock_start, mock_join, mock_terminate, mock_exit_code):
    mock_exit_code.return_value = 0

    def fn():
        time.sleep(3.0)

    mock_start.side_effect = fn

    assert _run(lambda: None, None)

    assert mock_terminate.called is False


@patch("time.sleep")
def test_loop(mock_sleep):
    mock = Mock()
    mock.side_effect = lambda: mock.call_count == 3

    _loop(mock, 0.0, False, 1.0)

    assert mock.call_count == 3


@patch("time.sleep")
def test_loop_reverse(mock_sleep):
    mock = Mock()
    mock.side_effect = lambda: mock.call_count > 3

    _loop(mock, 1.0, True, 1.0)

    assert mock.call_count == 1
