# -*- coding: utf-8 -*-
import time

from kit.rpc.middleware import Middleware


class RedisLockMiddleware(Middleware):
    """分布式锁"""

    def __init__(self, lock_key=None, lock_timeout=None, redis_client=None):
        if redis_client is None:
            raise ValueError("redis_client is required")
        self.lock_key = lock_key or "lock:job"
        self.lock_timeout = lock_timeout or 5
        self.redis = redis_client

    def before_callback(self, broker, message, *args, **kwargs):
        if message.failed:
            return
        while True:
            lock = self.redis.set(self.lock_key, 1, ex=self.lock_timeout, nx=True)
            if lock:
                break
            time.sleep(1)

    def after_callback(self, broker, message, *args, **kwargs):
        self.redis.delete(self.lock_key)

