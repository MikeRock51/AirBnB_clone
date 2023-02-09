#!/usr/bin/python3
"""Entry point of HBNB command interpreter"""

import cmd
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '

    def do_create(self, cls):
        """Creates a new instance of BaseModel"""
        pass

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
