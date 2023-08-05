# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Config(metaclass=ABCMeta):

    @abstractmethod
    def get(self, key, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def set(self, key, value, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def remove(self, key, *args, **kwargs):
        raise NotImplementedError
