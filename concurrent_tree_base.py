import threading
import time

class ConcurrentTreeBase:

    def __init__(self, parent=None):
        self.__parent = parent
        if parent is not None:
            self.mutex = parent.mutex
        else:
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

    def get_root(self):
        if self.__parent is not None:
            return self.__parent.get_root()
        else:
            return self

    def get_left(self):
        raise NotImplementedError()

    def get_right(self):
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
