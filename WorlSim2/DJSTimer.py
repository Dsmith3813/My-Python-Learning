'''
DJSTimer start
Usage:

with Timer(name='Name for this timmer'):
    <Code of what you want to have timed>
'''

from dataclasses import dataclass, field
from contextlib import ContextDecorator
from typing import Any, Callable, ClassVar, Dict, Optional
import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer(ContextDecorator):
    """Time your code."""

    timers: ClassVar[Dict[str, float]] = {}
    name: str = 'NoName'
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        def FT(seconds):
            return time.strftime("%H:%M:%S", time.gmtime(seconds))

        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if elapsed_time > 60:
            etime = FT(round(elapsed_time, 0))
        else:
            etime = f'{elapsed_time:.4f} seconds'

        print(f'>> {self.name} elapsed time: {etime}\n')

        return elapsed_time

    def __enter__(self) -> "Timer":
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer"""
        self.stop()

# DJStimer end
