# Inbuilt commands
import traceback
import os
import shutil

debug_mode = False


def debugtraceback():
    if debug_mode:
        traceback.print_exc()


class commands:
    def echo(arg):
        print(arg)
    
    def commandexists(*args):
        attribute = commands
        for i in args:
            hasattrbool = hasattr(attribute, i)
        if hasattrbool:
            print("Command exists.")
        if not hasattrbool:
            print("Command does not exist.")
    
    # It works enough, someone fix it for me pls B)
    def help(*args):
        attribute = commands
        for i in args:
            getattrout = getattr(attribute, i, "")
        print(dir(getattrout))
    
    def cwd(args=False):
        if not args:
            print(os.getcwd())
        elif not os.path.isdir(args):
            print("Invalid path.")
            debugtraceback()
        elif args:
            os.chdir(args)

    def debugmode(arg="status"):
        global debug_mode
        if arg == "on":
            debug_mode = True
            print("Debug mode on.")
        if arg == "off":
            debug_mode = False
            print("Debug mode off.")
        if arg == "status":
            print(f"Debug mode is {'on' if debug_mode else 'off'}.")

    class filetools:
        def mkdir(dir):
            try:
                os.mkdir(dir)
                print("Directory created.")
            except PermissionError:
                print("Permission denied.")
                debugtraceback()

        def copy(file, destination, recursive=False):
            try:
                if recursive in ["recursive", "r"]:
                    shutil.copytree(file, destination)
                elif not recursive:
                    shutil.copyfile(file, destination)
                else:
                    raise TypeError
                print("File copied.")
                debugtraceback()
            except shutil.SameFileError:
                print("The destination and the source file are the same.")
                debugtraceback()
            except IsADirectoryError:
                print(
                    """You are trying to copy a directory.
                    This requires the '--r' or '--recursive' argument."""
                )
                debugtraceback()
            except PermissionError:
                print("Permission is denied.")
                debugtraceback()
            except IOError:
                print("The destination is not writable.")
                debugtraceback()

        def move(file, destination):
            try:
                shutil.move(file, destination)
                print("File moved.")
            except NotADirectoryError:
                raise TypeError
            except shutil.SameFileError:
                print("The destination and the source file are the same.")
                debugtraceback()
            except PermissionError:
                print("Permission denied.")
                debugtraceback()
            except IOError:
                print("The destination is not writable.")
                debugtraceback()
