"""Implementation of a list of handlers."""
from asyncio import CancelledError, iscoroutinefunction
from dataclasses import dataclass
from multiprocessing import RLock
from typing import (
    Any,
    Callable,
    Coroutine,
    Final,
    Generic,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
import warnings
from typing_extensions import ParamSpec


import anyio

from .exceptions import CallWarning


_P = ParamSpec("_P")
_R = TypeVar("_R")


@dataclass
class _CallResult(Generic[_P, _R]):
    func: Callable[_P, _R]
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]


@dataclass
class SuccessCall(_CallResult[_P, _R], Generic[_P, _R]):
    """A successful call result item."""

    result: _R


@dataclass
class CallError(_CallResult[_P, _R], Generic[_P, _R]):
    """An error call result."""

    error: BaseException


class HandlerList(Generic[_P, _R]):
    """A list of callables.

    This implements a list of callables to be called in order.

    All callables receive only one parameter set and emit a list of results, either
    success or error.
    """

    def __init__(self, *, is_async: bool = False) -> None:
        super().__init__()
        self._callables: Final[
            List[
                Union[
                    Callable[_P, _R],
                    Callable[_P, Coroutine[Any, Any, _R]],
                ]
            ]
        ] = []
        self._once_callables = self._callables.copy()
        self._is_async = is_async
        self._lock = RLock()

    def __call__(self, *args: _P.args, **kwds: _P.kwargs) -> List[_CallResult[_P, _R]]:
        call_results: List[_CallResult[_P, _R]] = []
        callable_list = [*self._callables, *self._once_callables]

        for item in callable_list:
            self.remove_once(item)
            try:
                result: Optional[_R] = None
                if iscoroutinefunction(item):
                    if not self._is_async:
                        warnings.warn(
                            "Calling async code in non-async handler list is not "
                            "guaranteed to success.",
                            CallWarning,
                        )
                    result = anyio.from_thread.run(self._call_async, item, args, kwds)

                elif not iscoroutinefunction(item):
                    result = item(*args, **kwds)  # type: ignore
            except CancelledError:
                break
            except BaseException as exc:  # pylint: disable=broad-except
                call_result = CallError(
                    func=item,
                    args=args,
                    kwargs=kwds,
                    error=exc,
                )
            else:
                call_result = SuccessCall(
                    func=item,
                    args=args,
                    kwargs=kwds,
                    result=result,
                )
                call_results.append(call_result)  # type: ignore

        return call_results

    async def _call_async(
        self,
        func: Callable[..., Coroutine[Any, Any, _R]],
        args: Tuple[Any, ...],
        kwargs: Mapping[str, Any],
    ) -> _R:
        return await func(*args, **kwargs)

    def handler(
        self, func: Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]
    ) -> Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]:
        """Add an handler to the list.

        Args:
            func: The function to be added.

        Returns:
            The passed function
        """
        if func not in self._callables:
            with self._lock:
                self._callables.append(func)
        return func

    def once(
        self, func: Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]
    ) -> Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]:
        """Add an handler to the list to be called only once.

        Args:
            func: The function to be added.

        Returns:
            The passed function
        """
        if func not in self._once_callables:
            with self._lock:
                self._once_callables.append(func)
        return func

    def remove(
        self, func: Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]
    ) -> None:
        """Remove an handler, if present.

        Args:
            func: The handler to be removed.
        """
        if func in self._callables:
            with self._lock:
                self._callables.remove(func)

    def remove_once(
        self, func: Union[Callable[_P, _R], Callable[_P, Coroutine[Any, Any, _R]]]
    ) -> None:
        """Remove an handler, if present.

        Args:
            func: The handler to be removed.
        """
        if func in self._once_callables:
            with self._lock:
                self._once_callables.remove(func)
