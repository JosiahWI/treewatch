# Copyright (c) 2024 Josiah VanderZee

import threading
import time

class ConcurrentTreeBase:

    def __init__(self):
        self.mutex = threading.Lock()

    def is_selected(self):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def height(self):
        raise NotImplementedError()

    def add(self, value):
        raise NotImplementedError()

    def remove(self, value):
        raise NotImplementedError()

    def is_empty(self):
        return self.get_root() is None

    def get_root(self):
        raise NotImplementedError()

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def suspend(self):
        if not self.mutex.locked():
            raise RuntimeError("suspend called on already suspended tree")

        self.unlock()
        time.sleep(0.5)
        self.lock()

    def __enter__(self):
        self.lock()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unlock()

class Node:

    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right
        self._selected = False

    def is_selected(self):
        return self._selected

    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False
