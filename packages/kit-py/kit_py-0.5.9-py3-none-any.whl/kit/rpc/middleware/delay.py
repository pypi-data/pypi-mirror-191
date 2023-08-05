# -*- coding: utf-8 -*-
import random
import time

from kit.rpc.middleware import Middleware


class DelayMiddleware(Middleware):
    """执行函数前延迟中间件"""

    def __init__(self, delay_min=5, delay_max=10):
        """
        :param delay_min: 最小延迟时间
        :param delay_max: 最大延迟时间
        """
        assert delay_min <= delay_max, "delay_min must less than delay_max"
        self.delay_min = delay_min
        self.delay_max = delay_max

    def before_callback(self, broker, message, *args, **kwargs):
        if message.failed:
            return
        time.sleep(
            self.delay_min + (self.delay_max - self.delay_min) * random.random()
        )
