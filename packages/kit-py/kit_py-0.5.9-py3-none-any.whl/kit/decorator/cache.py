# -*- coding: utf-8 -*-
import time

def time_cache(timeout):
    def decorator(func):
        cache = {}

        def wrapper(*args, **kwargs):
            # 计算缓存键值
            key = args + tuple(kwargs.items())

            # 如果缓存有效，直接返回结果
            if key in cache and time.time() - cache[key][1] < timeout:
                return cache[key][0]

            # 计算并缓存结果
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        return wrapper
    return decorator



class count_cache:   # noqa

    def __init__(self, count):
        self.count = count
        self.cache = {}

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            use_count = self.cache.get('count', 0)
            if use_count < self.count - 1 and key in self.cache:
                self.cache['count'] += 1
                return self.cache[key]
            else:
                self.cache[key] = fn(*args, **kwargs)
                self.cache['count'] = 0
                return self.cache[key]

        return wrapper
