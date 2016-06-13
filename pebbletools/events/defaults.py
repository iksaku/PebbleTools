from libpebble2.protocol.music import *
from pebbletools.events import *


class ItunesControllerEvent(WindowsApplicationEvent):
    def __init__(self, pebble):
        super(ItunesControllerEvent, self).__init__(pebble, MusicControl, "iTunes.Application")

    def run(self, packet):
        if isinstance(packet, MusicControl) and self.is_app_running(by_class=None, app="iTunes"):
            key = None
            if isinstance(packet.data, MusicControlPlayPause):
                key = "  "
            elif isinstance(packet.data, MusicControlNextTrack):
                key = "^{RIGHT}"
            elif isinstance(packet.data, MusicControlPreviousTrack):
                key = "^{LEFT}"
            elif isinstance(packet.data, MusicControlVolumeUp):
                key = "^{UP}"
            elif isinstance(packet.data, MusicControlVolumeDown):
                key = "^{DOWN}"
            if key is not None:
                self.app_send_keys(by_class=None, app="iTunes", keys=key, switch_to_app=True, switch_back=True)


class PowerpointControllerEvent(WindowsApplicationEvent):
    class_name = None
    in_presentation = False

    def __init__(self, pebble):
        super(PowerpointControllerEvent, self).__init__(pebble, MusicControl, "PowerPoint")

    def run(self, packet):
        if self.class_name is None:
            for v in [7, 97, 9, 10, 11, 12, "T"]:
                if self.is_app_running("PP" + str(v) + "FrameClass", None):
                    self.class_name = "PP" + str(v) + "FrameClass"
                    break
        if isinstance(packet, MusicControl) and self.is_app_running(by_class=self.class_name, app=None):
            key = None
            if isinstance(packet.data, MusicControlPlayPause):
                key = "{ESC}" if self.in_presentation else "{F5}"
                self.in_presentation = not self.in_presentation
            elif isinstance(packet.data, MusicControlNextTrack):
                key = "{RIGHT}"
            elif isinstance(packet.data, MusicControlPreviousTrack):
                key = "{LEFT}"
            elif isinstance(packet.data, MusicControlVolumeUp):
                key = "{UP}"
            elif isinstance(packet.data, MusicControlVolumeDown):
                key = "{DOWN}"
            if key is not None:
                self.app_send_keys(by_class=self.class_name, app=None, keys=key, switch_to_app=False,
                                   switch_back=False)
