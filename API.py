import abc
from libpebble2.communication import PebbleConnection
from libpebble2.communication.transports.serial import SerialTransport
from libpebble2.protocol import *
from serial import SerialException
import time
import os.path


class Pebble(object):
    def __init__(self, port):
        try:
            self.handler = PebbleConnection(SerialTransport(port))
            self.handler.connect()
            self.handler.run_async()
        except SerialException:
            print "Could not connect to Pebble on port '" + port + "'"
            exit(1)

    def do_ping(self):
        self.handler.send_packet(PingPong(message=Ping(), cookie=53))
        self.handler.read_from_endpoint(PingPong)

    def update_time(self):
        print "Setting time to " + str(time.asctime())
        self.handler.send_packet(
            TimeMessage(message=SetUTC(unix_time=time.time(), utc_offset=-0600, tz_name="America/Monterrey")))


class Command(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, main, name, description, usage=""):
        self.main = main
        self.name = name
        self.description = description
        self.usage = usage

    @abc.abstractmethod
    def run(self, args=list):
        return


class CommandMap(object):
    def __init__(self, main):
        self.commands = {}
        self.main = main

    def register_command(self, command):
        self.commands[command.name] = command

    def register_commands(self, commands):
        for command in commands:
            self.register_command(command(self.main))

    def unregister_command(self, command):
        del self.commands[command.name]

    def run_command(self, name, args=list):
        cmd = self.commands.get(name)
        if isinstance(cmd, Command):
            self.main.debug("Executing command '" + name + "'")
            cmd.run(args)
        else:
            print "Unknown command '" + name + "'"


class Main(object):
    port = ""
    debug_enable = False

    def __init__(self):
        if not os.path.isfile("options.conf"):
            config = open("options.conf", "w")
            config.writelines("port: COM4\ndebug_enable: False")
            config.close()
        config = open("options.conf", "r")
        for line in config:
            key, value = line.replace(" ", "").replace("\n", "").split(":")
            if value == "True" or value == "False":
                value = bool(value)
            setattr(self, key, value)
        config.close()

        self.pebble = Pebble(self.port)
        self.commandMap = CommandMap(self)
        self.active = True

    def debug(self, message):
        if self.debug_enable:
            print message

    def stop(self):
        self.active = False
