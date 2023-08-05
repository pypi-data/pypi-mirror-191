# -*- coding: utf-8 -*-
import functools
import logging
import pdb
import threading
import time
import traceback

from .type_assert import type_assert


def singleton(cls):
    """
    单例模式装饰器
    >>> @singleton
    >>> class MyClass: pass
    """
    _instance = {}
    singleton.__lock = threading.Lock()

    @functools.wraps(cls)
    def _singleton(*args, **kwargs):
        if cls in _instance:
            return _instance[cls]
        with singleton.__lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kwargs)
            return _instance[cls]

    return _singleton


def time_it(func):
    @functools.wraps(func)
    def _timer(*args, **kwargs):
        t0 = time.perf_counter()
        back = func(*args, **kwargs)
        t1 = time.perf_counter()
        print(f"{func.__name__} took {t1 - t0:.0f} seconds")
        return back

    return _timer


def catch_error(return_val=None, log=True):
    """
    捕获异常装饰器
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.exception(e) if log else logging.debug(e)
                return return_val

        return wrapper

    return decorator


def except_debug(func):
    """
    跟踪调试函数装饰器
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pdb.set_trace()
            print(e)
            return func(*args, **kwargs)

    return wrapper


def running_in_thread(func):
    """
    函数在调用的时候会运行在单独的线程中

    >>> @running_in_thread
    >>> def runner():
    >>>     pass
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


class classproperty:
    """
    可以从类访问的属性的装饰器 来自于 django
    """

    def __init__(self, method=None):
        self.method = method

    def __get__(self, instance, cls=None):
        return self.method(cls)


class ExceptionContextManager:
    """
    上下文管理器捕获异常

    >>> with ExceptionContextManager(raise_exception=True) as e:
    >>>     print(1 / 0)
    """

    def __init__(self, logger_name='ExceptionContextManager', raise_exception=True):
        self.logger = logging.getLogger(logger_name)
        self.raise_exception = raise_exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.raise_exception:
            if exc_tb is not None:
                exc_str = str(exc_type) + '  :  ' + str(exc_val)
                exc_str_color = '\033[0;30;41m%s\033[0m' % exc_str
                self.logger.error('\n'.join(traceback.format_tb(exc_tb)) + exc_str_color)
        return self.raise_exception
