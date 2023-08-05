# -*- coding: utf-8 -*-
class Middleware:

    def before_send(self, broker, message, *args, **kwargs):
        """发送消息前执行"""

    def after_send(self, broker, message, *args, **kwargs):
        """发送消息后执行"""

    def before_callback(self, broker, message, *args, **kwargs):
        """处理消息前执行"""

    def after_callback(self, broker, message, result, *args, **kwargs):
        """处理消息后执行"""

