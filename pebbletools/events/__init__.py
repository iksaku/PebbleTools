from libpebble2.communication import PebbleConnection
import abc
import time
import win32com.client
import win32gui


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


class WindowsApplicationEvent(BaseEvent):
    app_pid = None

    def __init__(self, pebble, endpoint, app):
        super(WindowsApplicationEvent, self).__init__(pebble, endpoint)
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.shell.AppActivate(app)

    @abc.abstractmethod
    def run(self, packet):
        return

    def app_send_keys(self, by_class, app, keys, switch_to_app=True, switch_back=False):
        current = win32gui.GetForegroundWindow()
        if not self.is_app_running(by_class, app):
            return False
        self.app_pid = self.get_app_pid(by_class, app)
        if switch_to_app:
            if not self.app_focus(self.app_pid):
                return False
        self.shell.SendKeys(keys)
        if current != self.app_pid and switch_back:
            self.app_focus(current)
        return True

    def app_focus(self, app_pid, fix_alt="%"):
        if app_pid is None or app_pid < 1:
            return False
        if win32gui.GetForegroundWindow() != app_pid:
            self.shell.SendKeys("%")
            win32gui.SetForegroundWindow(app_pid)
            if fix_alt is str:
                self.shell.SendKeys(fix_alt)
        time.sleep(0.2)
        return True

    @staticmethod
    def get_app_pid(by_class, app):
        return win32gui.FindWindow(by_class, app)

    def is_app_running(self, by_class, app):
        return self.get_app_pid(by_class, app) > 0


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
