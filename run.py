from pebbletools import Main
from pebbletools.commands.defaults import *

print "Initializing..."
main = Main()
main.commandMap.register_commands({
    HelpCommand, PingCommand, StopCommand, TimeCommand
})
print "Ready to go! Type 'help' to list available commands"
while main.active:
    command = raw_input()
    args = command.split(" ")
    main.commandMap.run_command(args.pop(0), args)
