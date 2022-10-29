import os
import signal
import sys
from typing import Any, Callable


class Process:
    def __init__(
        self,
        target: Callable[..., Any],
        args: tuple[Any, ...] | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()

        self._target = target
        self._args: tuple[Any, ...] = args
        self._kwargs: dict[str, Any] = kwargs

        self._pid: int | None = None
        self._exit_code: int | None = None

    def start(self) -> None:
        self._pid = os.fork()

        if self._pid == 0:
            self._target(*self._args, **self._kwargs)
            sys.exit(0)

    def join(self) -> None:
        if self._pid is None:
            raise RuntimeError("process not started")

        _, exit_code = os.waitpid(self._pid, 0)

        self._exit_code = exit_code

    def terminate(self) -> None:
        if self._pid is None:
            raise RuntimeError("process not started")

        os.kill(self._pid, signal.SIGTERM)

    @property
    def exit_code(self) -> int | None:
        return self._exit_code
