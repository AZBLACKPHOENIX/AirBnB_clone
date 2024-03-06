#!/usr/bin/python3
import cmd
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
import re
import json


class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""

    prompt = '(hbnb) '

    def emptyline(self):
        """Called when an empty line is entered."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the shell."""
        print()
        return True

    def do_create(self, arg):
        """Create a new instance of a class."""
        if not arg:
            print("** class name missing **")
            return
        classes = ["BaseModel", "State", "City", "Amenity", "Place", "Review"]
        if arg not in classes:
            print("** class doesn't exist **")
            return
        new_obj = eval(arg)()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """Show the string representation of an instance."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in objs:
            print(objs[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy an instance."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in objs:
            del objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Show all instances or instances of a specific class."""
        args = arg.split()
        objs = storage.all()
        if len(args) == 0:
            print([str(v) for v in objs.values()])
            return
        if args[0] not in ["BaseModel", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        print([str(v) for k, v in objs.items() if k.split('.')[0] == args[0]])

    def do_update(self, arg):
        """Update an instance."""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in ["BaseModel", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key not in objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(objs[key], args[2], args[3].replace('"', '').replace(',', ''))
        objs[key].save()

    def do_count(self, arg):
        """Count instances of a class."""
        args = arg.split()
        counter = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                counter += 1
        print(counter)

    def default(self, arg):
        """Called on an unrecognized command."""
        m = re.match(r"([a-zA-Z_]+)\.([a-zA-Z_]+)\((.*)\)", arg)
        if m is None:
            print("*** Unknown syntax: {}".format(arg))
            return
        if m.group(1) not in ["BaseModel", "State", "City", "Amenity", "Place", "Review"]:
            print("*** Unknown syntax: {}".format(arg))
            return
        if m.group(2) == "all":
            self.do_all(m.group(1))
            return
        if m.group(2) == "show":
            self.do_show(m.group(1) + " " + m.group(3))
            return
        if m.group(2) == "destroy":
            self.do_destroy(m.group(1) + " " + m.group(3))
            return
        if m.group(2) == "count":
            self.do_count(m.group(1))
            return
        if m.group(2) == "update":
            update_str = m.group(1) + " " + m.group(3)
            self.do_update(update_str)
            return
        print("*** Unknown syntax: {}".format(arg))
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()

