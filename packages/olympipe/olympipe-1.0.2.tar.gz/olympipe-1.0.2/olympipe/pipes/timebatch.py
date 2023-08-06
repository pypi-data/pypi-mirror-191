import time
from multiprocessing import Queue
from typing import Iterable, List, Optional, TypeVar
from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class TimeBatchPipe(GenericPipe[R, Iterable[R]]):
    def __init__(
        self, source: "Queue[R]", target: "Queue[Iterable[R]]", interval: float
    ):
        self._interval: float = interval
        self._timeout: float = interval
        self._datas: List[R] = []
        self._last_time = time.time()
        super().__init__(source, target)

    def perform_task(self, data: R) -> Optional[Iterable[R]]:  # type: ignore
        elapsed = time.time() - self._last_time
        self._timeout = self._last_time + self._interval - time.time()
        if elapsed >= self._interval:
            self.increment_timeout()
            packet = self._datas[:]
            self._datas.clear()
            self._datas.append(data)
            return packet
        self._datas.append(data)
        return None

    def increment_timeout(self):
        self._last_time += self._interval
        self._timeout += self._interval

    def dispatch_to_next(self, processed: Iterable[R]):
        super().dispatch_to_next(processed)

    def run(self):
        while True:
            try:
                data = self._source.get(timeout=self._timeout)
                if GenericPipe.is_death_packet(data):
                    self.dispatch_to_next(self._datas)
                    self._datas = []
                    self._kill(data)
                    return
                processed = self.perform_task(data)
                if processed is not None:
                    self.dispatch_to_next(processed)

            except Exception:
                self.dispatch_to_next(self._datas)
                self._datas = []
                self.increment_timeout()
