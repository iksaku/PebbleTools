from libpebble2.communication import PebbleConnection
import abc


class BaseEvent(object):
    pebble = PebbleConnection
    _handler = None

    def __init__(self, pebble, endpoint):
        self.pebble = pebble
        self.endpoint = endpoint
        self.handler = self.pebble.register_endpoint(endpoint, self.run)

    def unregister(self):
        self.pebble.unregister_endpoint(self.handler)

    @abc.abstractmethod
    def run(self, packet):
        return


class EventManager(object):
    events = {}
    _default_events = {}

    def __init__(self, utils):
        self.utils = utils

    def register_event(self, event):
        handler = len(self.events)
        self.events[handler] = event(pebble=self.utils.handler)
        return handler

    def register_events(self, events):
        handlers = {}
        for event in events:
            handlers[self.register_event(event)] = event
        return handlers

    def unregister_event(self, handler):
        if handler in self.events:
            event = self.events.get(handler, None)
            if isinstance(event, BaseEvent):
                event.unregister()
            if event is not None:
                del self.events[handler]
