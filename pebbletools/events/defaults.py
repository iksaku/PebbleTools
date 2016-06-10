from libpebble2.protocol import MusicControl
from pebbletools.events import BaseEvent


class MusicControllerEvent(BaseEvent):
    def __init__(self, pebble):
        super(MusicControllerEvent, self).__init__(pebble, MusicControl)

    def run(self, packet):
        print packet
