# -*- coding: utf-8 -*-
from datetime import datetime
from queue import Queue, Empty

from croniter import croniter

from kit.rpc.broker import Broker
from kit.tool.timer import Timer


class CronBroker(Broker):

    def __init__(self, cron, name=None, middlewares=None, **kwargs):
        super().__init__(name=name, middlewares=middlewares)

        self.cron = cron
        self.itr = croniter(cron, datetime.now())
        self.next_fire_time = self.itr.get_next(datetime)
        self.kwargs = kwargs
        self.queue = Queue()
        self.timer = Timer("cron", self.do, interval=1)
        self.timer.scheduler()

    def do(self):
        if self.next_fire_time <= datetime.now():
            self.next_fire_time = self.itr.get_next(datetime)
            self.queue.put_nowait(self.kwargs)

    def consume(self, prefetch, timeout):
        return TimerConsume(self.queue, prefetch, timeout)

    def __repr__(self):
        return f"<CronBroker {self.name}>"


class TimerConsume:

    def __init__(self, queue, prefetch, timeout):
        self.queue = queue
        self.prefetch = prefetch
        self.timeout = timeout

    def __next__(self):
        try:
            return self.queue.get(timeout=self.timeout / 1000)
        except Empty:
            return None

    def __iter__(self):  # pragma: no cover
        return self

    def ack(self, *args, **kwargs): ...

    def nack(self, *args, **kwargs): ...