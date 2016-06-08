import abc


class Command(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, main, name, description, usage=""):
        self.main = main
        self.name = name
        self.description = description
        self.usage = usage

    def get_usage(self):
        return "Usage: " + self.name + " " + self.usage

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
            cmd.run(args)
        else:
            print "Unknown command '" + name + "'"
