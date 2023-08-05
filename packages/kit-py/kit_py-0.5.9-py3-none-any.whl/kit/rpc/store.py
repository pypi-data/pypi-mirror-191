# -*- coding: utf-8 -*-
global_store = None


def get_store():
    global global_store
    if global_store is None:
        try:
            from kit.store.rabbitmq import RabbitmqStore
        except ImportError:
            raise ImportError('pls install kit')

        rmq_store = RabbitmqStore(
            hostname='localhost',
            port=5672,
            username='admin',
            password='admin',
            virtual_host='/'
        )
        return rmq_store
    return global_store


def set_store(store):
    global global_store
    global_store = store
