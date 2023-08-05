# -*- coding: utf-8 -*-
import json

from . import Config
from kit.store.redis_ import RedisStore


class RedisConfig(Config):

    def __init__(self, url=None, *args, **kwargs):
        self.config_group = kwargs.pop('config_group', 'default.group')
        self.redis = RedisStore(url, *args, **kwargs)

    def get(self, key, *args, **kwargs) -> dict:
        value = self.redis.hash_get(name=self.config_group, key=key)
        return value

    def set(self, key, value, *args, **kwargs):
        return self.redis.hash_set(name=self.config_group, key=key, value=json.dumps(value))

    def remove(self, key, *args, **kwargs):
        self.redis.hash_del(name=self.config_group, key=key)

