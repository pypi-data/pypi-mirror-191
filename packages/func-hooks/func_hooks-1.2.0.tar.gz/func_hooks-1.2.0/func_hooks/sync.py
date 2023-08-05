"""Synchronous hooks implementation."""
import asyncio
from functools import partial
import typing
import warnings

import anyio
import typing_extensions

from func_hooks.handler_list import HandlerList

from .exceptions import CallWarning
from .typing import Invocation, InvocationError, InvocationResult

_P = typing_extensions.ParamSpec("_P")
_R = typing.TypeVar("_R")
_FR = typing.TypeVar("_FR")


class Hooks(typing.Generic[_P, _FR]):
    """A decorator for synchronous hooks."""

    def __init__(self, func: typing.Callable[_P, _FR]) -> None:
        super().__init__()

        self._func = func
        self.on_before: HandlerList[
            [Invocation[typing.Callable[_P, _FR]]], None
        ] = HandlerList(is_async=self.is_async)
        self.on_result: HandlerList[
            [typing.Mapping[str, typing.Any]], None
        ] = HandlerList(is_async=self.is_async)
        self.on_after: HandlerList[
            [InvocationResult[typing.Callable[_P, _FR], _FR]], None
        ] = HandlerList(is_async=self.is_async)
        self.on_error: HandlerList[
            [InvocationError[typing.Callable[_P, _FR]]], None
        ] = HandlerList(is_async=self.is_async)

        self._name = None

    @property
    def is_async(self):
        """Return wether the hooks are for an async function."""
        return asyncio.iscoroutinefunction(self._func)

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _FR:
        if not self.is_async:
            return self._run_sync(*args, **kwargs)  # type: ignore

        return anyio.to_thread.run_sync(  # type: ignore
            lambda args, kwargs: self._run_sync(*args, **kwargs), args, kwargs
        )

    def _run_sync(self, *args: _P.args, **kwargs: _P.kwargs) -> typing.Any:
        results: typing.Dict[str, typing.Any] = {
            "before_errors": [],
            "after_errors": [],
            "error_hook_errors": [],
            "success": False,
            "result": None,
        }
        results["before_errors"] = self._run_pre_hooks(
            Invocation(
                func=self._func,
                args=args,
                kwargs=kwargs,
            )
        )
        try:
            if self.is_async:
                results["result"] = anyio.from_thread.run(
                    lambda args, kwargs: self._func(*args, **kwargs),  # type: ignore
                    args,
                    kwargs,
                )
            else:
                results["result"] = self._func(*args, **kwargs)
        except Exception as exc:
            results["error_hook_errors"] = self._run_error_hooks(
                InvocationError(
                    func=self._func,
                    args=args,
                    kwargs=kwargs,
                    exception=exc,
                )
            )
            raise
        else:
            results["after_errors"] = self._run_post_hooks(
                InvocationResult(
                    func=self._func,
                    args=args,
                    kwargs=kwargs,
                    result=results["result"],  # type: ignore
                )
            )
        self._run_results_hook(results)
        return results["result"]  # type: ignore

    def _run_results_hook(self, results: typing.Dict[str, typing.Any]) -> None:
        self.on_result(results)

    def _run_pre_hooks(self, invocation: Invocation[typing.Any]):
        return self.on_before(invocation)

    def _run_post_hooks(
        self, invocation_result: InvocationResult[typing.Any, typing.Any]
    ):
        return self.on_after(invocation_result)

    def _run_hooks(
        self,
        invocation_result: typing.Any,
        hook_list: typing.List[typing.Callable[[typing.Any], typing.Any]],
    ):
        errors: typing.List[BaseException] = []

        for item in hook_list:
            try:
                if not asyncio.iscoroutinefunction(item):
                    item(invocation_result.copy())  # type: ignore
                else:
                    if not self.is_async:
                        warnings.warn_explicit(
                            (
                                f"The function {item!r} may not be called because the "
                                "hooks object is not for an async function."
                            ),
                            CallWarning,
                            item.__code__.co_filename,
                            item.__code__.co_firstlineno,
                        )
                    anyio.from_thread.run(item, invocation_result.copy())
            except BaseException as exc:  # pylint: disable=broad-except
                errors.append(exc)
                warnings.warn(f"Error while calling {item!r}: {exc!r}", CallWarning)
        return errors

    def _run_error_hooks(self, result: InvocationError[typing.Any]):
        return self.on_error(result)

    def on_results(
        self,
        func: typing.Union[
            typing.Callable[[typing.Mapping[str, typing.Any]], None],
            typing.Callable[
                [typing.Mapping[str, typing.Any]],
                typing.Coroutine[typing.Any, typing.Any, None],
            ],
        ],
    ) -> typing.Union[
        typing.Callable[[typing.Mapping[str, typing.Any]], None],
        typing.Callable[
            [typing.Mapping[str, typing.Any]],
            typing.Coroutine[typing.Any, typing.Any, None],
        ],
    ]:
        """A function to call on results.

        Args:
            func: The function that receives all results

        Returns:
            typing.Callable[[typing.Dict[str, typing.Any]], None]: The function itself
        """

        return self.on_result.handler(func)

    def __get__(
        self,
        obj: typing.Optional[object],
        objtype: typing.Optional[typing.Type[object]] = None,
    ):
        bound_hooks = None
        if obj is None:
            bound_hooks = self
        else:
            hooks_attrname = f"__hooks_{self._name}__"
            try:
                bound_hooks = getattr(obj, hooks_attrname)
            except AttributeError:
                from .decorator import hooks  # pylint: disable=import-outside-toplevel

                obj_hooks = partial(self, obj)
                bound_hooks = hooks(obj_hooks)
                setattr(obj, hooks_attrname, bound_hooks)

        return bound_hooks

    def __repr__(self) -> str:
        clsname = type(self).__name__
        return f"{clsname}({self._func!r})"

    def __set_name__(self, owner: typing.Type[object], name: str):
        self._name = name
