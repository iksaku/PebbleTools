from API import *
from Commands import *

main = Main()
main.commandMap.register_commands({
    HelpCommand, PingCommand, StopCommand
})
print "Ready!"
while main.active:
    command = raw_input()
    args = command.split(" ")
    main.commandMap.run_command(args.pop(0), args)
