# -*- coding: utf-8 -*-
import functools
import logging

logger = logging.getLogger(__name__)


class redis_lock(object):  # noqa
    """
    Distributed lock by redis
    """

    def __init__(self, key, timeout, shift=0, redis_client=None):
        self.key = key
        self.timeout = timeout + shift
        self.redis_client = redis_client

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"LOCK::{self.key}"
            value = "--lock--"
            if self.redis_client.set(key, value, self.timeout, nx=True):
                return func(*args, **kwargs)

            logger.info('locked %s, %s, just return', key, func)
            return False

        return wrapper
