#!/usr/bin/python3
"""Entry point of HBNB command interpreter"""

import cmd

class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '

    def do_EOF(self, line):
        """Quits the command interpreter when it receives EOF signal"""
        print()
        return True

    def do_quit(self, line):
        """Quits out of the command interpreter"""
        return True

    def emptyline(self):
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
