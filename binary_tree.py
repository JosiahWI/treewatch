from concurrent_tree_base import ConcurrentTreeBase

class BinarySearchTree(ConcurrentTreeBase):

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = None
        self.right = None
        self.value = value
        self._size = 1
        self.selected = False

    def is_selected(self):
        return self.selected

    def size(self):
        return self._size

    def height(self):
        if self.left is None and self.right is None:
            return 0
        elif self.left is None:
            return 1 + self.right.height()
        elif self.right is None:
            return 1 + self.left.height()
        else:
            return 1 + max(self.left.height(), self.right.height())

    def add(self, value):
        self.selected = True
        self._size += 1
        self.suspend()
        if value <= self.value:
            if self.left is not None:
                self.left.add(value)
            else:
                self.left = BinarySearchTree(value, parent=self)
        else:
            if self.right is not None:
                self.right.add(value)
            else:
                self.right = BinarySearchTree(value, parent=self)
        self.selected = False

    def remove(self, value):
        self.selected = True
        self.suspend()
        result = None
        if value == self.value:
            self.get_root()._size -= 1
            if self.right is not None:
                replace_with = self.right.__max()
                self.remove(replace_with.value)
                result =  replace_with
            else:
                result = self.left
        elif value < self.value:
            if self.left is not None:
                self.left = self.left.remove(value)
                result = self
        else:
            if self.right is not None:
                self.right = self.right.remove(value)
                result = self

        self.selected = False
        return result

    def __max(self):
        self.selected = True
        self.suspend()
        result = self
        if self.right is not None:
            result = self.right._max()
        self.selected = False
        return result


    def get_left(self):
        return self.left

    def get_right(self):
        return self.right
