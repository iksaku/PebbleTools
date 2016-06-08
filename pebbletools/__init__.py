from libpebble2.communication import PebbleConnection
from libpebble2.protocol import *
from serial import SerialException
from commands import *
import logging
import os.path
import time


class Pebble(object):
    def __init__(self, main):
        self.main = main
        try:
            log = logging.DEBUG if self.main.debug_enabled else None
            self.handler = PebbleConnection(self.main.transport(self.main.port), log, log)

            self.handler.connect()
            self.handler.run_async()
        except SerialException:
            print "Could not connect to Pebble"
            print "Trying '" + str(type(self.main.transport)) + "' on port '" + self.main.port + "'"
            exit(1)


class Main(object):
    port = ""
    debug_enabled = False

    def __init__(self):
        options_file = "../options.conf"
        if not os.path.isfile(options_file):
            config = open(options_file, "w")
            options = [
                "transport: SerialTransport",
                "port: COM4",
                "debug_enabled: False"
            ]
            config.write("\n".join(options))
            config.close()
        config = open(options_file, "r")
        for line in config:
            if line[:1] == "#":
                continue
            key, value = line.replace(" ", "").replace("\n", "").split(":")
            if "transport" in key:
                if "QEMU" in value:
                    from libpebble2.communication.transports.qemu import QemuTransport
                    value = QemuTransport
                elif "Websocket" in value:
                    from libpebble2.communication.transports.websocket import WebsocketTransport
                    value = WebsocketTransport
                else:
                    from libpebble2.communication.transports.serial import SerialTransport
                    value = SerialTransport
            elif "debug_enabled" in key:
                value = bool(value)
            setattr(self, key, value)
        config.close()

        self.pebble = Pebble(self)
        self.commandMap = CommandMap(self)
        self.active = True

    def stop(self):
        self.active = False

    """
    API!
    """

    def do_ping(self):
        self.pebble.handler.send_packet(PingPong(message=Ping(), cookie=53))
        self.pebble.handler.read_from_endpoint(PingPong)

    def update_time(self, utc_offset, tz_name):
        self.pebble.handler.send_packet(
            TimeMessage(message=SetUTC(unix_time=time.time(), utc_offset=utc_offset, tz_name=tz_name)))


class MusicController(object):
    def __init__(self, pebble):
        self.pebble = pebble

    def update_information(self, artist, album, title, track_length, track_count, current_track):
        self.pebble.handler.send_packet(MusicControl(data=MusicControlUpdateCurrentTrack(
            artist=artist, album=album, title=title,
            track_length=track_length, track_count=track_count, current_track=current_track)
        ))


