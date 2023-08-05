# -*- coding: utf-8 -*-
import logging
import json
import random
from inspect import isgenerator
from typing import List, Optional

from .broker import Broker
from .message import Message
from .worker import _ConsumerThread

from .events import events as global_events, Events
from kit.tool import gen_unique_id

logger = logging.getLogger(__name__)


class Job:

    def __init__(self,
                 fn,
                 job_id=None,
                 from_broker=None, to_broker=None,
                 config=None,
                 events=None,
                 retry_times=None,
                 workers=None):
        self.fn = fn
        self.job_id = job_id or gen_unique_id()

        self.from_brokers = self._init_brokers(from_broker)
        self.to_broker = self._init_brokers(to_broker)
        self.config = config
        self.retry_times = retry_times
        self.workers = workers
        # 合并全局事件和局部事件
        self.events = (events or Events()) + global_events
        for broker in self.from_brokers:
            broker.job = self
            self._add_consumer(broker)
        self.events.emit("job_init", job=self)

    @staticmethod
    def _init_brokers(broker) -> List[Broker]:
        """
        由于broker其实是支持多进多出的，
        为适配单个broker，和多个broker的情况，统一将broker转为列表
        """
        if broker is None:
            return []
        elif isinstance(broker, Broker):
            return [broker]
        elif isinstance(broker, list):
            return broker
        else:
            raise TypeError("broker must be Broker or list of Broker")

    def send(self, message, broker=None):
        if message is None:
            logger.debug("send message is None")
            return
        if not self.to_broker and not broker:
            logger.debug("send broker is None")
            return
        _brokers = self._init_brokers(broker) or self.to_broker

        for broker in _brokers:
            try:
                _config = self._get_config(broker) or {}
            except Exception as e:
                logger.warning(f"Failed to get config: {e}")
                _config = {}
            _message = Message(message)
            # 外部的配置优先级高于内部的配置
            kwargs = {**_config, **(_message.message.get("kwargs", {}) or {})}
            _message.message['kwargs'] = kwargs
            self._post_message(broker, _message)

    def _post_message(self, broker, message):
        self.events.emit("job_send", job=self, broker=broker, message=message)
        broker.before_emit("send", message=message)
        if not message.failed:
            # 如果需要格式转换，需要实现broker的`format_message`方法，默认原样输出。
            real_message = broker.format_message(message.message)
            broker.send(real_message)
        else:
            logger.warning(f"Failed to send message: {message.exc_info}")
        broker.after_emit("send", message=message)

    def _add_consumer(self, broker):
        self.events.emit("job_add_consumer", job=self, broker=broker)
        for _ in range(self.workers):
            consumer = _ConsumerThread(
                fn=self,
                broker=broker,
                prefetch=1,
                worker_timeout=1000,
                retry_times=self.retry_times
            )
            consumer.start()

    def _get_config(self, broker: Broker) -> Optional[dict]:
        if not self.config:
            return

        if not (cfg := self.config.get(str(broker))):
            return

        try:
            return json.loads(cfg)
        except json.JSONDecodeError:
            return

    def __call__(self, message, *args, **kwargs):
        """当作为函数调用时，执行fn"""
        res = self.fn(message, *args, **kwargs)
        if isgenerator(res):
            for item in res:
                self.send(item)
        else:
            self.send(res)
        return res

    def __repr__(self):
        return f"<Job {self.job_id}>"


class JobMixin:

    def job(self,
            job_class=Job,
            job_id=None,
            from_broker=None,
            to_broker=None,
            config=None,
            events=None,
            retry_times=0,
            workers=1):
        """
        任务装饰器
        :param job_class: 任务类
        :param job_id: 任务id
        :param from_broker: 从哪个broker消费
        :param to_broker: 发送到哪个broker
        :param config: 配置中心
        :param events: 当前job的局部自定义事件
        :param retry_times: 重试次数
        :param workers: 消费者数量
        :return:
        """

        def decorator(fn):
            return job_class(fn,
                             job_id=job_id,
                             from_broker=from_broker,
                             to_broker=to_broker,
                             config=config,
                             events=events,
                             retry_times=retry_times,
                             workers=workers)

        return decorator

    def register_events(self, **events):
        for name, event in events.items():
            global_events.on(name, event)
