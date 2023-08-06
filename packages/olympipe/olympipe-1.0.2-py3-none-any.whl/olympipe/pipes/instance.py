from multiprocessing import Queue
from typing import TypeVar, Dict, List, Any, Callable
from multiprocessing.managers import BaseManager
from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")


class ClassInstancePipe(GenericPipe[R, S]):
    def __init__(
        self,
        source: "Queue[R]",
        constructor_class: Any,
        use_method: Callable[[Any, R], S],
        target: "Queue[S]",
        args_class: List[Any] = [],
        kwargs_class: Dict[str, Any] = {},
    ):
        BaseManager.register(constructor_class.__name__, constructor_class)
        self._instance = constructor_class(*args_class, **kwargs_class)
        self._task = getattr(self._instance, use_method.__name__)
        super().__init__(source, target)

    def perform_task(self, data: R) -> S:
        return self._task(data)
