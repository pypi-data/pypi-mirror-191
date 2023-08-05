from queue import Queue, Empty

from kit.rpc.broker import Broker


class MemoryBroker(Broker):
    def __init__(self, queue=None, middlewares=None):
        # 创建本地队列
        if queue is None:
            queue = Queue()
        self.queue = queue
        super().__init__(queue=self.queue, middlewares=middlewares)

    def send(self, message):
        self.queue.put_nowait(message)

    def consume(self, *args, **kwargs):
        return MemoryConsume(self.queue, *args, **kwargs)

    def __repr__(self):
        return f"<QueueBroker: {self.queue}>"


class MemoryConsume:

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

    def ack(self, *args, **kwargs):
        ...

    def nack(self, *args, **kwargs):
        ...