from pebbletools import Main

print "Initializing..."
main = Main()
print "Ready to go! Type 'help' to list available commands"
while main.active:
    command = raw_input()
    args = command.split(" ")
    main.commandMap.run_command(args.pop(0), args)
