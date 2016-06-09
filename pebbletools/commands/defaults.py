from pebbletools.commands import Command
import time


class HelpCommand(Command):
    def __init__(self, main):
        super(HelpCommand, self).__init__(main, "help", "Show commands and usage", "[command]")

    def run(self, args=list):
        message = []
        commands = self.main.commandMap.commands
        if isinstance(args, list) and isinstance(commands, dict):
            if len(args) > 0:
                cmd_name = args.pop(0)
                cmd = commands.get(cmd_name)
                if isinstance(cmd, Command):
                    message.append("Description: " + cmd.description)
                    message.append(cmd.get_usage())
                    message.append("Help for command '" + cmd.name + "'")
                else:
                    message = "Unknown command '" + cmd_name + "'"
            else:
                for name, cmd in sorted(commands.iteritems()):
                    if isinstance(cmd, Command):
                        message.append(cmd.name)
                message.append("Available commands:")
        if type(message) == list:
            message = message.pop(len(message) - 1) + "\n\t" + "\n\t".join(message)
        print message


class MusicTestCommand(Command):
    def __init__(self, main):
        super(MusicTestCommand, self).__init__(main, "musictest", "Fills sample data for Pebble's Music App")

    def run(self, args=list):
        print "Filling sample data to Music app..."
        self.utils.music_information("iksaku", "MusicTestCommand", "PebbleTools", (1*60 + 34)*1000, 15, 1)


class PingCommand(Command):
    def __init__(self, main):
        super(PingCommand, self).__init__(main, "ping", "Pings your Pebble watch")

    def run(self, args=list):
        self.utils.do_ping()


class StopCommand(Command):
    def __init__(self, main):
        super(StopCommand, self).__init__(main, "stop", "Stops the tool from running")

    def run(self, args=list):
        print "Quitting..."
        self.main.stop()


class TimeCommand(Command):
    def __init__(self, main):
        super(TimeCommand, self).__init__(
            main, "time", "Updates your pebble's time", "<time difference with UTC> <time zone name>")

    def run(self, args=list):
        if isinstance(args, list):
            if len(args) < 2:
                print self.get_usage()
            else:
                print "Setting time to: " + time.asctime()
                print "Offset: " + args[0]
                print "Time Zone name: " + args[1]
                self.utils.update_time(int(args[0]), args[1])
