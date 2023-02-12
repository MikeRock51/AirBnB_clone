#!/usr/bin/python3
"""Entry point of HBNB command interpreter"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from ast import literal_eval
import re


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = '(hbnb) '

    def do_create(self, class_name):
        """Creates a new instance of BaseModel"""

        if not class_name:
            print("** class name missing **")
        elif globals().get(class_name) is None:
            print("** class doesn't exist **")
        else:
            instance = storage.class_list()[class_name]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance"""

        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif f"{line[0]}.{line[1]}" not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[f"{line[0]}.{line[1]}"])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""

        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif f"{line[0]}.{line[1]}" not in storage.all():
            print("** no instance found **")
        else:
            del (storage.all()[f"{line[0]}.{line[1]}"])

    def do_all(self, class_name):
        """Prints all string representation of all instances"""

        if not class_name:
            print(list(str(instance) for instance in storage.all().values()))
        else:
            if globals().get(class_name) is None:
                print("** class doesn't exist **")
            else:
                print(list(str(instance) for instance in storage.all(
                ).values() if type(instance).__name__ == class_name))

    def do_update(self, line):
        """Updates an instance based on the class name and id"""

        # Usage: update <class name> <id> <attribute name> "<attribute value>"
        line = line.split()
        if len(line) < 1:
            print("** class name missing **")
        elif globals().get(line[0]) is None:
            print("** class doesn't exist **")
        elif len(line) < 2:
            print("** instance id missing **")
        elif f"{line[0]}.{line[1]}" not in storage.all():
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

    def default(self, line):
        ''' implements the default commands  '''
        objects = storage.all().values()
        argv = line.split('.', 1)

        if len(argv) != 2 or argv[0] not in storage.class_list():
            print('*** unknown syntax:', line)
            return

        if argv[0] in storage.class_list() and argv[1].endswith('()'):
            command = argv[1][:-2]

            if command not in ['all', 'count']:
                print('*** unknown syntax:', line)
                return

            if command == 'all':
                attrs = \
                    [obj for obj in objects if type(obj).__name__ == argv[0]]
                [print(att, end=', ' if att != attrs[-1] else '\n')
                    for att in attrs]
                return

            if command == 'count':
                count = 0
                for obj in objects:
                    if type(obj).__name__ == argv[0]:
                        count += 1
                print(count)
                return

        cls_name = argv[0]
        param = re.search(r"\((.*?)\)", argv[1])
        attributes = re.search(r"\{(.*?)\}", param[1])

        if param:
            method = argv[1][:param.span()[0]]
            param_list = param[1].split(', ', 2)
            id = param_list[0][1:-1]
            if len(param_list) == 1:
                line = ' '.join([cls_name, id])
                eval('self.do_' + method)(line)
            elif not attributes:
                param_list = ' '.join(param_list)
                line = ' '.join([cls_name, param_list])
                eval('self.do_' + method)(line)
            else:
                param_list = param[1].split(', ', 1)
                attr_dict = param_list[1].replace("'", '"')
                line = ' '.join([cls_name, id, attr_dict])
                eval('self.do_' + method)(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
