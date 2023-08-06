from multiprocessing import Queue
from typing import Iterable, List, Optional, TypeVar
from .generic import GenericPipe

R = TypeVar("R")


class BatchPipe(GenericPipe[R, Iterable[R]]):
    def __init__(self, source: "Queue[R]", target: "Queue[Iterable[R]]", count: int):
        super().__init__(source, target)
        self._count = count
        self._datas: List[R] = []

    def perform_task(self, data: R) -> Optional[Iterable[R]]:  # type: ignore
        self._datas.append(data)
        if len(self._datas) >= self._count:
            packet, self._datas = self._datas[: self._count], self._datas[self._count :]
            return packet

    def dispatch_to_next(self, processed: Iterable[R]) -> None:
        if processed is None:
            return
        super().dispatch_to_next(processed)
