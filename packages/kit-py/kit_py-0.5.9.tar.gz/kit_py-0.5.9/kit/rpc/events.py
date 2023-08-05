# -*- coding: utf-8 -*-


class Events:

    def __init__(self):
        self._events = {}

    def on(self, event, fn):
        self._events.setdefault(event, []).append(fn)

    def emit(self, event, **kwargs):
        if not event.startswith('on_'):
            event = f'on_{event}'
        for fn in self._events.get(event, []):
            fn(**kwargs)

    def remove(self, event, fn):
        self._events.get(event, []).remove(fn)

    def all(self):
        return self._events

    def __add__(self, other):
        _events = Events()
        combined_keys = self._events.keys() | other._events.keys()
        _events._events = {key: self._events.get(key, []) + other._events.get(key, []) for key in combined_keys}
        return _events


events = Events()
