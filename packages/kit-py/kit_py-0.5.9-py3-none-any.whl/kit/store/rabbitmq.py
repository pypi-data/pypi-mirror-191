# -*- coding: utf-8 -*-
import logging
from threading import local
from queue import PriorityQueue
import amqpstorm
from amqpstorm import AMQPConnectionError

MAX_SEND_ATTEMPTS = 6  # 最大发送重试次数
MAX_CONNECTION_ATTEMPTS = 6 # 最大连接重试次数

logger = logging.getLogger(__name__)


def heartbeat(fn):
    def wrapper(store: "RabbitmqStore", *args, **kwargs):
        if not store.connection or not store.connection.is_open:
            logger.warning("Connection is closed, reconnecting...")
            del store.connection
            if not store.connection:
                logger.warning('RabbitmqStore connection is closed, reconnecting...')
                return False
        return fn(store, *args, **kwargs)

    return wrapper


class RabbitmqStore:

    def __init__(self, *, confirm_delivery=False, host=None, port=None, username=None, password=None,
                 **kwargs):
        """
        :param confirm_delivery: 是否开启消息确认
        :param host: RabbitMQ host
        :param port: RabbitMQ port
        :param username: RabbitMQ username
        :param password: RabbitMQ password
        :param kwargs: RabbitMQ parameters
        """
        self.state = local()
        self.parameters = {
            'hostname': host or 'localhost',
            'port': port or 5672,
            'username': username or 'guest',
            'password': password or 'guest',
        }
        if kwargs:
            self.parameters.update(kwargs)
        self.confirm_delivery = confirm_delivery

    def _create_connection(self):
        attempts = 1
        while attempts <= MAX_CONNECTION_ATTEMPTS:
            try:
                return amqpstorm.Connection(**self.parameters)
            except AMQPConnectionError as exc:
                attempts += 1
                logger.warning("RabbitmqStore connection error: %s", exc)
        raise AMQPConnectionError("RabbitmqStore connection error, max attempts reached")

    @property
    def connection(self):
        connection = getattr(self.state, "connection", None)
        if connection is None or not connection.is_open:
            connection = self.state.connection = self._create_connection()
        return connection

    @connection.deleter
    def connection(self):
        if _connection := getattr(self.state, "connection", None):
            _connection.close()
            del self.state.connection
            del self.state.channel

    @property
    def channel(self):
        connection = getattr(self.state, "connection", None)
        channel = getattr(self.state, "channel", None)
        if all([connection, channel]) and all([connection.is_open, channel.is_open]):
            return channel
        channel = self.state.channel = self.connection.channel()
        if self.confirm_delivery:
            channel.confirm_deliveries()
        return channel

    @property
    def consumer_class(self):
        return _RabbitmqConsumer

    def consume(self, queue_name, prefetch=1, timeout=0):
        self.declare_queue(queue_name)
        return self.consumer_class(self, queue_name, prefetch=prefetch)

    def declare_queue(self, queue_name, arguments=None):
        """声明队列"""
        if arguments is None:
            arguments = {}
        return self.channel.queue.declare(queue_name, durable=True, arguments=arguments)

    def send(self, queue_name, message, priority=None, **kwargs):
        """发送消息"""
        attempts = 1
        while True:
            try:
                self.declare_queue(queue_name)
                self.channel.basic.publish(
                    message, queue_name, properties=priority, **kwargs
                )
                return message
            except Exception as exc:
                del self.connection
                attempts += 1
                if attempts > MAX_SEND_ATTEMPTS:
                    raise exc

    def flush_queue(self, queue_name):
        """清空队列"""
        self.channel.queue.purge(queue_name)

    def get_message_counts(self, queue_name: str) -> int:
        """获取消息数量"""
        queue_response = self.declare_queue(queue_name)
        return queue_response.get("message_count", 0)


class _RabbitmqConsumer:

    def __init__(self, instance, queue_name=None, prefetch=1):
        self.instance = instance
        self.queue_name = queue_name
        self.prefetch = prefetch
        self.message_queue = PriorityQueue()

    def __next__(self):
        try:
            self.receive()
        except AMQPConnectionError:
            print('AMQPConnectionError')
            del self.instance.connection
        except Exception as exc:
            print(exc)
            return None
        if self.message_queue.empty():
            return None
        message = self.message_queue.get()
        return message

    def receive(self, **kwargs):
        for _ in range(self.prefetch):
            message = self.instance.channel.basic.get(self.queue_name, **kwargs)
            if message is None:
                break
            self.message_queue.put(message)

    def ack(self, message):
        message.ack()

    def nack(self, message, requeue=False):
        message.nack(requeue=requeue)

    def __iter__(self):  # pragma: no cover
        return self
