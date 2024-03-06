#!/usr/bin/python3
"""Module for the HBNBCommand class."""
import cmd
import re
import json

from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

class HBNBCommand(cmd.Cmd):
    """Command interpreter class for HBNB project."""
    
    prompt = '(hbnb) '
    __classes = {
        'BaseModel',
        'Amenity',
        'Place',
        'User',
        'State',
        'Review',
        'City'
    }

    def emptyline(self):
        """Do nothing when empty line is entered."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Exit the program on EOF."""
        print()
        return True

    def do_create(self, args):
        """Create a new instance of a class."""
        if not args:
            print('** class name missing **')
            return

        class_name = args.split()[0]
        if class_name not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
            return

        new_instance = eval(f"{class_name}()")
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        """Show the string representation of an instance."""
        args = line.split()
        if len(args) == 0:
            print('** class name missing **')
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        key = "{}.{}".format(class_name, args[1])
        if key in storage.all():
            print(storage.all()[key])
        else:
            print('** no instance found **')

    def do_destroy(self, line):
        """Delete an instance."""
        args = line.split()
        if len(args) == 0:
            print('** class name missing **')
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        key = "{}.{}".format(class_name, args[1])
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print('** no instance found **')

    def do_all(self, args):
        """Show all instances."""
        if not args:
            print([str(v) for v in storage.all().values()])
        else:
            class_name = args.split()[0]
            if class_name in HBNBCommand.__classes:
                instances = [str(v) for k, v in storage.all().items() if v.__class__.__name__ == class_name]
                print(instances)
            else:
                print('** class doesn\'t exist **')

    def do_update(self, args):
        """Update an instance."""
        args = split(args)
        if not args:
            print('** class name missing **')
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return

        key = "{}.{}".format(class_name, args[1])
        if key not in storage.all():
            print('** no instance found **')
            return

        if len(args) < 3:
            print('** attribute name missing **')
            return

        if len(args) < 4:
            print('** value missing **')
            return

        attr_name = args[2]
        attr_value = args[3]
        instance = storage.all()[key]
        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_count(self, line):
        """Count instances of a class."""
        args = line.split()
        if not args:
            print('** class name missing **')
            return

        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print('** class doesn\'t exist **')
            return

        count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == class_name)
        print(count)

    def default(self, line):
        """Default command handling."""
        cmd, arg = line.split('.', 1)
        arg = arg.strip()

        if cmd == 'update':
            arg_split = arg.split(',')
            key = "{}.{}".format(arg_split[0], arg_split[1])
            if key in storage.all():
                obj = storage.all()[key]
                try:
                    attrs = json.loads(arg_split[2])
                    for k, v in attrs.items():
                        setattr(obj, k.strip(), v)
                    obj.save()
                except ValueError:
                    pass

        elif cmd == 'all':
            class_name = arg.split('(')[0]
            if class_name in HBNBCommand.__classes:
                instances = [str(v) for k, v in storage.all().items() if v.__class__.__name__ == class_name]
                print(instances)
            else:
                print('** class doesn\'t exist **')

        elif cmd == 'show':
            class_name, obj_id = arg.split('(')[0].split(',')
            obj_id = obj_id.strip().strip('"')
            key = "{}.{}".format(class_name, obj_id)
            if key in storage.all():
                print(storage.all()[key])
            else:
                print('** no instance found **')

        elif cmd == 'destroy':
            class_name, obj_id = arg.split('(')[0].split(',')
            obj_id = obj_id.strip().strip('"')
            key = "{}.{}".format(class_name, obj_id)
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print('** no instance found **')

        elif cmd == 'count':
            class_name = arg.strip().strip('"')
            count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == class_name)
            print(count)

        else:
            print('*** Unknown syntax: {}'.format(line))

    def postloop(self):
        """Print newline after exiting."""
        print()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
