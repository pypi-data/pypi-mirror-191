# -*- coding: utf-8 -*-
import logging
import time
from threading import Thread, Event


logger = logging.getLogger(__name__)


class _ConsumerThread(Thread):

    def __init__(self, fn, broker, prefetch, worker_timeout, retry_times=3):
        super().__init__(daemon=True)
        self.job_callback = fn
        self.events = fn.events
        self.running = False
        self.consumer = None
        self.broker = broker
        self.paused = False
        self.paused_event = Event()
        self.prefetch = prefetch
        self.worker_timeout = worker_timeout
        self.retry_times = retry_times

    def run(self):
        self.running = True
        while self.running:
            if self.paused:
                self.paused_event.set()
                time.sleep(self.worker_timeout / 1000)
                continue

            self.consumer = self.broker.consume(
                prefetch=self.prefetch,
                timeout=self.worker_timeout,
            )
            for message in self.consumer:
                if message is not None:
                    # 自定义broker的消息处理类
                    message = self.broker.message_class(message)
                    self.events.emit('on_receive', job=self.job_callback, message=message)
                    self.broker.before_emit("callback", message=message)
                    try:
                        result = self._run_job_callback(message)
                    except Exception as e:
                        logger.error(f'Failed to run fn: {e}')
                        message.fail(e)
                        self.events.emit('on_job_error', job=self.job_callback, message=message, error=e)
                        continue
                    self.broker.after_emit("callback", message=message, result=result)

    def _run_job_callback(self, message):
        """
        job_callback(message=message.message, options=message.options)
        message:
            为了下游接收到的直接是MQ中的消息，而不是AMQPMessage对象，提前解构出来
        options:
            从message中解构出来，方便下游使用
        """
        _retry_times = 0
        while True:
            _retry_times += 1
            try:
                if message.failed:
                    logger.error(f'Failed to run fn: {message.exc_info}')
                    self.events.emit('on_job_error', job=self.job_callback, message=message, error=message.exc_info)
                    self.consumer.nack(message.original_message)
                    return

                res = self.job_callback(message=message.message, options=message.options)
                self.consumer.ack(message.original_message)
                return res
            except Exception as e:
                logger.error(f'Failed to run fn: {e}，retry times: {_retry_times}')
                # message.fail(e)
                self.events.emit('on_job_error', job=self.job_callback, message=message, error=e)
                if _retry_times > self.retry_times:
                    self.consumer.nack(message.original_message)
                    return
                continue
