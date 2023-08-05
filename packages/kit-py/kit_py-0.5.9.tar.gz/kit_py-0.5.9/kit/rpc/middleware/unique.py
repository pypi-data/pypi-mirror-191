# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import List

from kit.rpc.message import Message
from kit.rpc.middleware import Middleware
from redis.client import Redis

CHECKER = namedtuple(
    'checker',
    ['func', 'error_msg', 'state']
)

class UniqueMiddleware(Middleware):
    """
    在发往下一个broker前，对字段进行唯一校验。
    只有满足唯一字段的数据才会被成功发送

    当func检查为False，且state小于0时，此条消息将会被废弃
    """

    def __init__(self, key=None, redis_client=None):
        if redis_client is None:
            raise ValueError("")
        self.key = key or 'default_key'
        self.redis: Redis = redis_client

    def before_send(self, broker, message: Message, *args, **kwargs):
        err, state = self._check(message.message)
        if state and int(state) < 0:
            message.fail(err)

    def get_checkers(self, message) -> List[CHECKER]:
        raise NotImplementedError

    def _check(self, message):
        for check in self.get_checkers(message):
            if not check.func():
                return check.error_msg, check.state
        return None, None

