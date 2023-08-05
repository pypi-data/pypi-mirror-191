# -*- coding: utf-8 -*-
import logging
import json
from dataclasses import dataclass, field
from typing import Any

from amqpstorm.message import Message as AmqpMessage
from kit.dict import Dict

logger = logging.getLogger(__name__)


@dataclass
class MessageSchema:
    message: Any
    options: dict = field(default_factory=dict)


class _Message:
    def __init__(self):
        self.failed = False
        self.exc_info = ''
        self.options = Dict()

    def fail(self, exc_info=None):
        self.exc_info = exc_info or ''
        self.failed = True


class AMQPMessage(_Message):

    def __init__(self, message: AmqpMessage):
        super().__init__()
        self._message = message

    @property
    def original_message(self):
        return self._message

    @property
    def body(self):
        return self._message.body

    @property
    def message_id(self):
        return self._message.message_id

    @property
    def delivery_tag(self):
        return self._message.delivery_tag

    @property
    def message(self):
        try:
            return Dict(json.loads(self.body))
        except json.JSONDecodeError:
            logger.warning(f"Failed to decode message: {self.body}")
            return {}


class Message(_Message):

    def __init__(self, message: Any):
        super().__init__()
        self._message = message
        self.message = Dict(self._message)

    @property
    def original_message(self):
        return self._message

    def asdict(self):
        return Dict(self._message)

    def asstr(self):
        return json.dumps(self._message)

    def __repr__(self):
        return f"<Message>"
