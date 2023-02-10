#!/usr/bin/python3
"""Entry point of HBNB command interpreter"""

import cmd
from models.base_model import BaseModel
from models import storage
from ast import literal_eval


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '

    def do_create(self, class_name):
        """Creates a new instance of BaseModel"""

        if not class_name:
            print("** class name missing **")
        elif globals().get(class_name) is None:
            print("** class doesn't exist ** ")
        else:
            instance = storage.class_list()[class_name]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Prints the string representation of an
        instance based on the class name and id"""

        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif not f"{line[0]}.{line[1]}" in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{line[0]}.{line[1]}"])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)."""

        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif not f"{line[0]}.{line[1]}" in storage.all():
            print("** no instance found **")
        else:
            del (storage.all()[f"{line[0]}.{line[1]}"])

    def do_all(self, class_name):
        """Prints all string representation of all
        instances based or not on the class name"""

        if not class_name:
            print(list(str(instance) for instance in storage.all().values()))
        else:
            if globals().get(class_name) is None:
                print("** class doesn't exist **")
            else:
                print(list(str(instance) for instance in storage.all(
                ).values() if type(instance).__name__ == class_name))

    def do_update(self, line):
        """ Updates an instance based on the
        class name and id by adding or updating attribute """

        # Usage: update <class name> <id> <attribute name> "<attribute value>"
        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif not f"{line[0]}.{line[1]}" in storage.all():
            print("** no instance found **")
        elif len(line) < 3:
            print("** attribute name missing **")
        elif len(line) < 4:
            print("** value missing **")
        else:
            class_name = line[0]
            instance_id = line[1]
            attribute_name = line[2]
            attribute_value = literal_eval(line[3])

            instance = storage.all()[f"{class_name}.{instance_id}"]
            setattr(instance, attribute_name, attribute_value)
            instance.save()

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
