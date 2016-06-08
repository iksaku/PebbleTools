from .api import Command


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
                    message.append("Usage: " + cmd.name + " " + cmd.usage)
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


class PingCommand(Command):
    def __init__(self, main):
        super(PingCommand, self).__init__(main, "ping", "Pings your Pebble watch")

    def run(self, args=list):
        self.main.pebble.do_ping()


class StopCommand(Command):
    def __init__(self, main):
        super(StopCommand, self).__init__(main, "stop", "Stops the tool from running")

    def run(self, args=list):
        print "Quitting..."
        self.main.stop()
