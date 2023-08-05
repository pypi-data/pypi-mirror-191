# -*- coding: utf-8 -*-
import json

from kit.rpc.store import get_store
from .base import Broker
from ..message import AMQPMessage


class RMQBroker(Broker):

    def __init__(self, queue, backend_store=None, middlewares=None):
        super().__init__(queue=queue, backend_store=backend_store, middlewares=middlewares)
        self.backend_store = backend_store or self._get_default_store()

    def send(self, message):
        self.backend_store.send(self.queue, message)

    def consume(self, *args, **kwargs):
        return self.backend_store.consume(self.queue, *args, **kwargs)

    def format_message(self, message):
        """转换message的数据类型"""
        if not isinstance(message, str):
            return json.dumps(message)
        return message

    @staticmethod
    def _get_default_store():
        return get_store()

    @property
    def message_class(self):
        return AMQPMessage

    def __repr__(self):
        return f"<RMQBroker {self.queue}>"
