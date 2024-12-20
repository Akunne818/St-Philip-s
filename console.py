import cmd
from datetime import datetime
import models
import shlex
from models.base_models import Basemodels
from models.admin import Admin
from models.service import *
import models.service as service_module
import inspect

# Add all classes from models.service to the dictionary
classes = {
    "Admin": Admin
}

for name, obj in inspect.getmembers(service_module):
    # Check if the object is a class and is defined in the service module
    if inspect.isclass(obj) and obj.__module__ == service_module.__name__:
        # Add the class to the classes dictionary
        classes[name] = obj

class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(Church) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value

        return new_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)

            if args[0] == 'Admin':
                print(instance)
                instance.add_admin()
            

        else:
            print("** class doesn't exist **")
            return False

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        if len(args) < 3:
            print("** missing **", end="")
            if len(args) == 0:
                print("class name")
            elif len(args) == 1:
                print("instance id")
            else:
                print("attribute name")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False
        key = args[0] + "." + args[1]
        if key not in models.storage.all():
            print("** no instance found **")
            return False
        try:
            if args[0] == "Place":
                if args[2] in ["number_rooms", "number_bathrooms", "max_guest", "price_by_night"]:
                    args[3] = int(args[3])
                elif args[2] in ["latitude", "longitude"]:
                    args[3] = float(args[3])
            setattr(models.storage.all()[key], args[2], args[3])
            models.storage.all()[key].save()
        except ValueError:
            print("** value error **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
