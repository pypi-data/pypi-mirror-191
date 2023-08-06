#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from time import sleep
from typing import Type, Callable, Dict, Any, Tuple, Union

from ._hook import _get_chain, _run_hook_func
from .._internal import _T
from .._internal._method_helper import run_call_back
from ..log._factory import LoggerFactory

__logger = LoggerFactory.get_logger("retry")


def retry(frequency: int = 1, interval: int = 1, increasing: int = 0, check: Callable[[_T], bool] = lambda r: r,
          ignore_exception: Union[Type[Exception], Tuple[Type[Exception]]] = None,
          post_hook: Callable[[_T, _T], None] = None):
    """
    Provides retry functionality, if function run success, will run once.
    unit second

    callback functions can and only support communication via the chain keyword parameter. example: callback() is ok,
    callback(chain=None) is ok, callback(chain=None, other=None) is ok(other arg will not be assigned),
    callback(other, chain=None) will happened exception

    :param check: Check whether the result is as expected, return the result if it is met, otherwise try again.
    :param ignore_exception: If it is the exception and its child exceptions, no retry is made
    :param post_hook: If the original function is not executed.Two parameters are required, func_params and func_return
    the callback function is executed and the result of the callback function is returned,
    arguments to the original function are passed to the callback function
    :param frequency: number of executions.
    :param interval: retry interval, unit seconds.
    :param increasing: The incrementing interval
    """

    def _inner(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            interval_ = interval
            chain, func_new_kwargs = _get_chain(func, args, kwargs)
            for _ in range(1, frequency+1):
                # noinspection PyBroadException
                try:
                    result = func(*args, **kwargs)
                    if check(result):
                        return result
                    else:
                        __logger.log(level=30, msg=f"check result fail!!!", stacklevel=3)
                    __logger.log(level=20, msg=f"run function '{func.__name__}' "
                                               f"fail: retrying {_} time(s)", stacklevel=3)
                    sleep(interval_)
                    interval_ += increasing
                except BaseException as e:
                    if ignore_exception and issubclass(type(e), ignore_exception):
                        break
                    __logger.log(level=20, msg=f"run function '{func.__name__}' exception {type(e).__name__}: {str(e)}."
                                               f" retrying {_} time(s)", stacklevel=3)
                    sleep(interval_)
                    interval_ += increasing
            else:
                if post_hook:
                    _run_hook_func([post_hook], chain, func_new_kwargs)

        return _wrapper

    return _inner


def retrying(func: Callable, func_kwargs: Dict = None, frequency: int = 1, interval: int = 1, increasing: int = 0,
             check: Callable[[_T], bool] = lambda r: r,
             ignore_exception: Union[Type[Exception], Tuple[Type[Exception]]] = None,
             post_hook: Callable[[_T, _T], None] = None):
    """
    if function run success, will run once.
    :param func: The function to be retried.
    :param func_kwargs: The parameters of the function to be retried must be provided as keyword arguments.
    :param check: Check whether the result is as expected, return the result if it is met, otherwise try again.
    :param ignore_exception: If it is the exception and its child exceptions, no retry is made
    :param post_hook: If the original function is not executed.Two parameters are required, func_params and func_return
    the callback function is executed and the result of the callback function is returned,
    arguments to the original function are passed to the callback function
    :param frequency: number of executions.
    :param interval: retry interval.
    :param increasing: The incrementing interval
    :return:
    """
    for _ in range(1, frequency+1):
        try:
            if func_kwargs:
                result = func(**func_kwargs)
            else:
                result = func()
            if check(result):
                return result
            else:
                __logger.log(level=30, msg=f"check result fail!!!", stacklevel=3)
            __logger.log(level=20, msg=f"run function '{func.__name__}' "
                                       f"fail: retrying {_} time(s)", stacklevel=3)
            sleep(interval)
            interval += increasing
        except BaseException as e:
            if ignore_exception and issubclass(type(e), ignore_exception):
                break
            __logger.log(level=20, msg=f"run function '{func.__name__}' exception {type(e).__name__}: {str(e)}. "
                                       f"retrying {_} time(s)", stacklevel=3)
            sleep(interval)
            interval += increasing
    else:
        if post_hook:
            if func_kwargs:
                run_call_back(post_hook, func, tuple(), func_kwargs)
            else:
                post_hook({}, {})


def repeat(frequency: int = 1, interval: int = 1, increasing: int = 0,
           ignored_exception: Union[Type[Exception], Tuple[Type[Exception]]] = None):
    """
    Repeat the function, return last result.
    :param frequency: number of executions
    :param interval: the time between executions, unit seconds
    :param increasing: the incrementing interval
    :param ignored_exception:
                if happened exception and exception not included in ignored_exception will interrupt execution
    :return: last execute result
    """
    def _inner(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            interval_ = interval
            result = None
            for _ in range(1, frequency + 1):
                # noinspection PyBroadException
                try:
                    result = func(*args, **kwargs)
                except BaseException as e:
                    __logger.log(level=40,
                                 msg=f"run '{func.__name__}(args={args}, kwargs={kwargs}), ' happened exception, "
                                     f"result={result}, exception={str(e)}, run {_} time(s).", stacklevel=3)
                    if ignored_exception and not issubclass(e.__class__, ignored_exception):
                        raise
                finally:
                    __logger.log(level=20, msg=f"run '{func.__name__}(args={args}, kwargs={kwargs}), "
                                               f"result={result}, run {_} time(s).", stacklevel=3)
                if _ == frequency:
                    break
                sleep(interval_)
                interval_ += increasing
            return result
        return _wrapper

    return _inner


def repeating(func, frequency: int = 1, interval: int = 1, increasing: int = 0,
              ignored_exception: Union[Type[Exception], Tuple[Type[Exception]]] = None,
              args: Tuple = None, kwargs: Dict = None) -> Any:
    """
    Repeat the function, return last result
    :param func: the function to execute
    :param frequency: number of executions
    :param interval: the time between executions, unit seconds
    :param increasing: the incrementing interval
    :param ignored_exception:
                    if happened exception and exception not included in ignored_exception will interrupt execution
    :param args: func needs args
    :param kwargs: func needs kwargs
    :return: last execute result
    """
    result = None
    args_ = []
    kwargs_ = {}
    if args:
        args_.extend(args)
    if kwargs:
        kwargs_.update(kwargs)
    for _ in range(1, frequency + 1):
        # noinspection PyBroadException
        try:
            result = func(*args_, **kwargs_)
        except BaseException as e:
            __logger.log(level=40, msg=f"run '{func.__name__}(args={args}, kwargs={kwargs})' happened exception, "
                                       f"result={result}, exception={str(e)}, run {_} time(s).", stacklevel=3)
            if ignored_exception and not issubclass(e.__class__, ignored_exception):
                raise
        finally:
            __logger.log(level=20, msg=f"run '{func.__name__}(args={args}, kwargs={kwargs})', "
                                       f"result={result}, run {_} time(s).", stacklevel=3)
        if _ == frequency:
            break
        sleep(interval)
        interval += increasing
    return result


__all__ = [retry, retrying, repeat, repeating]
