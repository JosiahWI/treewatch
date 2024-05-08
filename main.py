#!/usr/bin/env python3

import re
import threading

from binary_tree import BinarySearchTree
import gui

root_value = int(input("Please enter a value to initialize the tree: "))

tree = BinarySearchTree(root_value)

init_complete = False

def init_callback():
    global init_complete
    init_complete = True

gui_thread = threading.Thread(target=gui.start_gui, args=(tree,init_callback))
gui_thread.start()

# This busy wait is not the most efficient way to do this, but for this
# toy application I think it'll suffice for now. A better solution could
# be to set a semaphore or something and wait on that.
while not init_complete:
    pass

while not (cmd := input("[add <i>, remove <i>, quit]: ")).startswith("q"):
    if cmd.startswith("add"):
        if re.match("^add \d+$", cmd) is None:
            print("Ill-formed add command.")
            continue
        value = int(cmd.split()[1])
        with tree:
            tree.add(value)
    elif cmd.startswith("remove"):
        if re.match("^remove \d+$", cmd) is None:
            print("Ill-formed remove command.")
            continue
        value = int(cmd.split()[1])
        with tree:
            tree.remove(value)
    else:
        print(f"Unrecognized command \"{cmd}\".")

print("Finished. Please click the X on the GUI to finish shutting down if you haven't already done so.")
gui_thread.join()
