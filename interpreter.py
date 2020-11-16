# Dependencies
import os
import readline
import inbuiltcommands
from platform import python_version


# Version, and other miscellanious variables
class miscobjs:
    version = "0.2-beta"  # Change before commit!


version = miscobjs.version

# Interpreter
while True:
    rawInput = str(
        input(
            "\033[92m\u001b[1minterpreter {} on Python {} {}\033[0m » ".format(
                version, python_version(), "\u001b[34m" + os.getcwd() + "\033[0m"
            )
        )
    )
    
    # Credits to Transfusion for this part!
    quoted_string_stack = []
    quotes_begin_end = [] # begin and end of string range that needs to be merged
    # cleanedInput = ""

    cmdArray = []
    argArray = []

    try:
        for idx, c in enumerate(rawInput):
            # print(idx, quoted_string_stack, quotes_begin_end)
            if c == '\'' or c == '"':
                if not quoted_string_stack or quoted_string_stack[0][1] != c:
                    quoted_string_stack.append((idx, c))
                else:
                    # can be simplified...
                    while quoted_string_stack[-1][1] != c:
                        quoted_string_stack.pop()
                    begin_idx, _ = quoted_string_stack[-1]
                    quoted_string_stack.pop()
                    quotes_begin_end.append((begin_idx, idx))

        quoted_args_begin_end = [(begin-2, end+1) for begin, end in
            filter(lambda x: rawInput[x[0]-2: x[0]] == '--', quotes_begin_end)]

        quoted_args_begin_end.insert(0, (0,0))
        quoted_args_begin_end.append((len(rawInput), len(rawInput)))

        for i in range(0, len(quoted_args_begin_end)-1):
            cleanedInput = rawInput[quoted_args_begin_end[i][1]: quoted_args_begin_end[i+1][0]]
            cleanedInput = cleanedInput.split()
            for s in cleanedInput:
                if s.startswith('--'):
                    argArray.append(s[2:])
                else:
                    cmdArray.append(s)

            if i < len(quoted_args_begin_end) - 2: # because we appended (len(rawInput), len(rawInput))
                # rawInput is echo --huehue --'hi hi' --"'ho ho' --'hee hee'" 'ha ha' --huhu
                # argArray is ['huehue', "--'hi hi'", '--"\'ho ho\' --\'hee hee\'"', 'huhu'], strip --" .... "
                argArray.append(rawInput[quoted_args_begin_end[i+1][0] + 3: quoted_args_begin_end[i+1][1] - 1])
    except:
        print("Invalid syntax.")
        traceback.print_exc()
    
    for b in cmdArray:
        if "--" in b:
            argArray.append(b)
            cmdArray = list(filter(lambda x: x not in argArray, cmdArray))
            argArray.append(b[2:])
    execute = inbuiltcommands.commands
    if inbuiltcommands.debug_mode:
        print("cmdArray: {} argArray: {}".format(cmdArray, argArray))
    for o in cmdArray:
        execute = getattr(execute, o, "")
    try:
        if inbuiltcommands.debug_mode:
            print(
                """
============================
           OUTPUT
============================
"""
            )
        execute(*argArray)
    except TypeError as syntaxerror:
        print("Invalid syntax.")
        print(syntaxerror)
        inbuiltcommands.debugtraceback()
