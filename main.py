#!/usr/bin/env python3

# Copyright (c) 2024 Josiah VanderZee

import re
import threading

from binary_tree import BinarySearchTree
import gui

tree = BinarySearchTree()

init_complete = False

def init_callback():
    global init_complete
    init_complete = True

def console_loop():
    # This busy wait is not the most efficient way to do this, but for this
    # toy application I think it'll suffice for now. A better solution could
    # be to set a semaphore or something and wait on that.
    while not init_complete:
        pass

    while not (cmd := input("[add <i>, remove <i>, q(uit)]: ")).startswith("q"):
        if cmd.startswith("add"):
            if re.match(r"^add -?\d+$", cmd) is None:
                print("Ill-formed add command.")
                continue
            value = int(cmd.split()[1])
            with tree:
                tree.add(value)
        elif cmd.startswith("remove"):
            if re.match(r"^remove -?\d+$", cmd) is None:
                print("Ill-formed remove command.")
                continue
            value = int(cmd.split()[1])
            with tree:
                tree.remove(value)
        else:
            print(f"Unrecognized command \"{cmd}\".")

    print("Finished. Please click the X on the GUI to finish shutting down if you haven't already done so.")

console_thread = threading.Thread(target=console_loop)
console_thread.start()

# The GUI must run on the main thread.
# (https://github.com/google-deepmind/pysc2/issues/2)
gui.start_gui(tree, init_callback)

console_thread.join()
