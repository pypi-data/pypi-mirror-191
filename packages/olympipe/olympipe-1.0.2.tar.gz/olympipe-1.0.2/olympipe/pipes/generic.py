import time
from multiprocessing import Process, Queue
from queue import Empty
from threading import Timer
from typing import Any, Generic, Optional, TypeVar, cast

R = TypeVar("R")
S = TypeVar("S")


class GenericPipe(Process, Generic[R, S]):
    __kill_word: Any = Empty

    def __init__(self, source: "Queue[R]", target: "Queue[S]"):
        super().__init__(daemon=True)
        self._source = source
        self._target = target
        self._timeout: Optional[float] = None
        Timer(0.01, self.start).start()

    @staticmethod
    def is_death_packet(p: Any) -> bool:
        try:
            return p[0] is GenericPipe.__kill_word
        except Exception:
            return False

    @staticmethod
    def get_kill_word(count: int = 1) -> Any:
        return (GenericPipe.__kill_word, count)

    def _close_source(self):
        try:
            self._source.close()
        except Exception:
            pass

    def _kill(self, data: Any):
        while not self._target.empty():
            time.sleep(0.01)
        self._close_source()
        self._target.put(data)

    def perform_task(self, data: R) -> S:
        return cast(S, data)

    def dispatch_to_next(self, processed: S):
        self._target.put(processed)

    def run(self):
        while True:
            try:
                data = self._source.get(timeout=self._timeout)
                if GenericPipe.is_death_packet(data):
                    self._kill(data)
                    return
                processed = self.perform_task(data)
                self.dispatch_to_next(processed)
            except Exception as e:
                self._kill(GenericPipe.get_kill_word())
                print(f"Error_{e.__class__.__name__}_{e.args}")
                return
