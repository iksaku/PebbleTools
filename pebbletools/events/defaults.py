from libpebble2.protocol.music import *
from pebbletools.events import *


class ItunesControllerEvent(WindowsApplicationEvent):
    def __init__(self, pebble):
        super(ItunesControllerEvent, self).__init__(pebble, MusicControl, "iTunes.Application")

    def run(self, packet):
        if isinstance(packet, MusicControl):
            if isinstance(packet.data, MusicControlPlayPause):
                self.shell.SendKeys(" ")
            elif isinstance(packet.data, MusicControlNextTrack):
                self.shell.SendKeys("^{RIGHT}")
            elif isinstance(packet.data, MusicControlPreviousTrack):
                self.shell.SendKeys("^{LEFT}")
            elif isinstance(packet.data, MusicControlVolumeUp):
                self.shell.SendKeys("^{UP}")
            elif isinstance(packet.data, MusicControlVolumeDown):
                self.shell.SendKeys("^{DOWN}")


class PowerpointControllerEvent(WindowsApplicationEvent):
    in_presentation = False

    def __init__(self, pebble):
        super(PowerpointControllerEvent, self).__init__(pebble, MusicControl, "PowerPoint")

    def run(self, packet):
        if isinstance(packet, MusicControl):
            if isinstance(packet.data, MusicControlPlayPause):
                self.shell.SendKeys("{ESC}" if self.in_presentation else "{F5}")
                self.in_presentation = not self.in_presentation
            elif self.in_presentation:
                if isinstance(packet.data, MusicControlNextTrack):
                    self.shell.SendKeys("{RIGHT}")
                elif isinstance(packet.data, MusicControlPreviousTrack):
                    self.shell.SendKeys("{LEFT}")
                elif isinstance(packet.data, MusicControlVolumeUp):
                    self.shell.SendKeys("{UP}")
                elif isinstance(packet.data, MusicControlVolumeDown):
                    self.shell.SendKeys("{DOWN}")
