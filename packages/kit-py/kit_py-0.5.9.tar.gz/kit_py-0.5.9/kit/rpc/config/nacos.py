# -*- coding: utf-8 -*-
import nacos

from . import Config


class NACOSConfig(Config):

    def __init__(self, server_addresses, **kwargs):
        self.config_group = kwargs.pop("config_group", "DEFAULT_GROUP")
        self.client = nacos.NacosClient(server_addresses, **kwargs)

    def set(self, key, value, **kwargs):
        return self.client.publish_config(data_id=key, group=self.config_group, content=value, **kwargs)

    def get(self, key, **kwargs):
        return self.client.get_config(data_id=key, group=self.config_group, **kwargs)

    def remove(self, key, **kwargs):
        return self.client.remove_config(data_id=key, group=self.config_group)

