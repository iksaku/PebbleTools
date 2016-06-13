from libpebble2.exceptions import *
from libpebble2.protocol import *
from libpebble2.services.notifications import Notifications
from pebbletools.commands import *
from pebbletools.commands.defaults import *
from pebbletools.events import *
from serial import SerialException
import logging
import time


class Utils(object):
    handler = PebbleConnection

    def __init__(self, main):
        self.main = main
        try:
            log = logging.DEBUG if self.main.debug_enabled else None
            self.handler = PebbleConnection(
                transport=self.main.transport(self.main.get_port), log_protocol_level=log, log_packet_level=log)

            self.handler.connect()
            self.handler.run_async()
        except SerialException:
            print "Could not connect to Pebble via SerialTransport"
            print "Trying on port '" + self.main.get_port + "'"
            exit(1)

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
    _default_commands = {
        HelpCommand,
        ItunesCommand,
        MusicTestCommand,
        NotificationCommand,
        PingCommand,
        PowerpointCommand,
        StopCommand,
        TimeCommand
    }
    port = ""
    debug_enabled = False

    def __init__(self):
        options_file = "options.conf"
        config = None
        try:
            config = open(options_file, "r")
        except IOError:
            config = open(options_file, "w")
            transport = raw_input(
                "Please provide a Transport to connect your Pebble from: (Serial*, QEMU, Websocket) ").lower()
            if "QEMU" in transport:
                transport = "QEMU"
            elif "Websocket" in transport:
                transport = "Websocket"
            else:
                if not ("Serial" in transport):
                    print "Unknown transport provided, using SerialTransport as default..."
                transport = "Serial"
            port = raw_input("What port do you wish to use? ")
            debug_enabled = raw_input("Would you like to enable Debug logging? (y/N*) ")
            if "y" in debug_enabled:
                debug_enabled = "True"
            else:
                debug_enabled = "False"
            options = [
                "transport: " + transport,
                "port: " + port,
                "debug_enabled: " + debug_enabled
            ]
            config.write("\n".join(options))
            config.close()
            config = open(options_file, "r")
        finally:
            if config is not None:
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
                        self.transport = value
                    elif "port" in key:
                        self.port = value
                    elif "debug_enabled" in key:
                        self.debug_enabled = bool(value)
                config.close()

        self.utils = Utils(main=self)
        self.commandManager = CommandManager(main=self)
        self.commandManager.register_commands(self._default_commands)
        self.eventManager = EventManager(utils=self.utils)

    @property
    def get_port(self):
        return self.port

    @property
    def is_running(self):
        return self._running

    def stop(self):
        self._running = False
