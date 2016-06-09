from libpebble2.communication import PebbleConnection
from libpebble2.exceptions import *
from libpebble2.protocol import *
from libpebble2.services.notifications import Notifications
from serial import SerialException
from commands import *
from commands.defaults import *
import logging
import os.path


class Utils(object):
    _handler = PebbleConnection

    def __init__(self, main):
        self.main = main
        try:
            log = logging.DEBUG if self.main.debug_enabled else None
            self.handler = PebbleConnection(
                transport=self.main.transport(self.main.get_port), log_protocol_level=log, log_packet_level=log)

            self.handler.connect()
            self.handler.run_async()
        except SerialException:
            print "Could not connect to Pebble"
            print "Trying '" + str(type(self.main.transport)) + "' on port '" + self.main.port + "'"
            exit(1)

    @property
    def get_pebble(self):
        return self._handler

    def do_ping(self):
        try:
            print self.handler.send_and_read(packet=PingPong(message=Ping(), cookie=53), endpoint=PingPong)
        except TimeoutError:
            print "Pong reception Timeout"

    def music_information(self, artist, album, title, track_length, track_count, current_track):
        self.handler.send_packet(MusicControl(data=MusicControlUpdateCurrentTrack(
            artist=artist, album=album, title=title,
            track_length=track_length, track_count=track_count, current_track=current_track)
        ))

    def send_notification(self, subject, message, sender):
        notification = Notifications(self.handler)
        notification.send_notification(subject=subject, message=message, sender=sender)

    def update_time(self, utc_offset, tz_name):
        self.handler.send_packet(
            TimeMessage(message=SetUTC(unix_time=time.time(), utc_offset=utc_offset, tz_name=tz_name)))


class Main(object):
    _running = True
    port = ""
    debug_enabled = False
    _default_commands = {
        HelpCommand,
        PingCommand,
        MusicTestCommand,
        NotificationCommand,
        StopCommand,
        TimeCommand
    }

    def __init__(self):
        options_file = "options.conf"
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
            print value
        config.close()

        self.utils = Utils(main=self)
        self.commandMap = CommandMap(self)
        self.commandMap.register_commands(self._default_commands)

    @property
    def get_port(self):
        return self.port

    @property
    def is_running(self):
        return self._running

    def stop(self):
        self._running = False
