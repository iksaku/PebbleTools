from pebbletools.commands import BaseCommand
import time


class HelpCommand(BaseCommand):
    def __init__(self, utils):
        super(HelpCommand, self).__init__(utils, "help", "Show commands and usage", "[command]")

    def run(self, args=list):
        message = []
        commands = self.utils.main.commandManager.commands
        if isinstance(args, list) and isinstance(commands, dict):
            if len(args) > 0:
                cmd_name = args.pop(0)
                cmd = commands.get(cmd_name)
                if isinstance(cmd, BaseCommand):
                    message.append("Description: " + cmd.description)
                    message.append(cmd.get_usage())
                    message.append("Help for command '" + cmd.name + "'")
                else:
                    message = "Unknown command '" + cmd_name + "'"
            else:
                for name, cmd in sorted(commands.iteritems()):
                    if isinstance(cmd, BaseCommand):
                        message.append(cmd.name)
                message.append("Available commands:")
        if type(message) == list:
            message = message.pop(len(message) - 1) + "\n\t" + "\n\t".join(message)
        print message


class MusicTestCommand(BaseCommand):
    def __init__(self, utils):
        super(MusicTestCommand, self).__init__(utils, "musictest", "Fills sample data for Pebble's Music App")

    def run(self, args=list):
        print "Filling sample data to Music app..."
        self.utils.music_information("iksaku", "MusicTestCommand", "PebbleTools", (1*60 + 34)*1000, 15, 1)


class NotificationCommand(BaseCommand):
    def __init__(self, utils):
        super(NotificationCommand, self).__init__(utils, "notification", "Sends a notification to your Pebble")

    def run(self, args=list):
        print "Let's build your notification! (Press Enter to leave field empty)"
        sender = raw_input("\tPlease identify the 'Sender': ")
        subject = raw_input("\tWhich is your 'Subject'? ")
        message = raw_input("\tEnter your 'Message': ")
        print "Sending your notification..."
        self.utils.send_notification(sender=sender, subject=subject, message=message)


class PingCommand(BaseCommand):
    def __init__(self, utils):
        super(PingCommand, self).__init__(utils, "ping", "Pings your Pebble watch")

    def run(self, args=list):
        self.utils.do_ping()


class StopCommand(BaseCommand):
    def __init__(self, utils):
        super(StopCommand, self).__init__(utils, "stop", "Stops the tool from running")

    def run(self, args=list):
        print "Quitting..."
        self.utils.main.stop()


class TimeCommand(BaseCommand):
    def __init__(self, utils):
        super(TimeCommand, self).__init__(
            utils, "time", "Updates your pebble's time", "<time difference with UTC> <time zone name>")

    def run(self, args=list):
        if isinstance(args, list):
            if len(args) < 2:
                print self.get_usage()
            else:
                print "Setting time to: " + time.asctime()
                print "Offset: " + args[0]
                print "Time Zone name: " + args[1]
                self.utils.update_time(int(args[0]), args[1])
