import abc


class BaseCommand(object):
    def __init__(self, utils, name, description, usage=""):
        self.utils = utils
        self.name = name
        self.description = description
        self.usage = usage

    def get_usage(self):
        return "Usage: " + self.name + " " + self.usage

    @abc.abstractmethod
    def run(self, args=list):
        return


class CommandManager(object):
    commands = {}

    def __init__(self, main):
        self.main = main

    def register_command(self, command):
        command = command(self.main.utils)
        self.commands[command.name] = command

    def register_commands(self, commands):
        for command in commands:
            self.register_command(command)

    def unregister_command(self, command):
        if command in self.commands:
            del self.commands[command.name]

    def run_command(self, name, args=list):
        cmd = self.commands.get(name)
        if isinstance(cmd, BaseCommand):
            cmd.run(args)
        else:
            print "Unknown command '" + name + "'"
