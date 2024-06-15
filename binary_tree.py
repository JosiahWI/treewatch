# Copyright (c) 2024 Josiah VanderZee

from concurrent_tree_base import ConcurrentTreeBase, Node

class BinarySearchTree(ConcurrentTreeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = None
        self._size = 0

    def size(self):
        return self._size

    def height(self):
        if not self.is_empty():
            return self.__height_of(self.get_root())
        else:
            return 0

    def __height_of(self, node):
        if node.left is None and node.right is None:
            return 0
        elif node.left is None:
            return 1 + self.__height_of(node.right)
        elif node.right is None:
            return 1 + self.__height_of(node.left)
        else:
            return 1 + max(self.__height_of(node.left),
                           self.__height_of(node.right))

    def add(self, value):
        self._size += 1
        if not self.is_empty():
            self.__add_to(self.get_root(), value)
        else:
            self._root = Node(value, None, None)

    def __add_to(self, node, value):
        node.select()
        self.suspend()
        if value <= node.value:
            if node.left is not None:
                self.__add_to(node.left, value)
            else:
                node.left = Node(value, None, None)
        else:
            if node.right is not None:
                self.__add_to(node.right, value)
            else:
                node.right = Node(value, None, None)
        node.unselect()

    def remove(self, value):
        if not self.is_empty():
            self._root = self.__remove_from(self.get_root(), value)
            self._size -= 1

    def __remove_from(self, node, value):
        node.select()
        self.suspend()
        result = node
        if value == node.value:
            if node.right is not None:
                min_node = self.__min_child_of(node.right)
                self.right = self.__remove_from(node, min_node.value)
                self.suspend()
                node.value = min_node.value
            else:
                result = node.left
        elif value < node.value:
            if node.left is not None:
                node.left = self.__remove_from(node.left, value)
        else:
            if node.right is not None:
                node.right = self.__remove_from(node.right, value)
        node.unselect()
        return result

    def __min_child_of(self, node):
        node.select()
        self.suspend()
        result = node
        if node.left is not None:
            result = self.__min_child_of(node.left)
        node.unselect()
        return result

    def get_root(self):
        return self._root

class AVLTree(ConcurrentTreeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root = None
        self._size = 0

    def size(self):
        return self._size

    def height(self):
        if not self.is_empty():
            return self.__height_of(self.get_root())
        else:
            return 0

    def __height_of(self, node):
        if node.left is None and node.right is None:
            return 0
        elif node.left is None:
            return 1 + self.__height_of(node.right)
        elif node.right is None:
            return 1 + self.__height_of(node.left)
        else:
            return 1 + max(self.__height_of(node.left),
                           self.__height_of(node.right))

    def add(self, value):
        self._size += 1
        if not self.is_empty():
            self.__add_to(self.get_root(), value)
        else:
            self._root = Node(value, None, None)

    def __add_to(self, node, value):
        node.select()
        self.suspend()
        if value <= node.value:
            if node.left is not None:
                self.__add_to(node.left, value)
            else:
                node.left = Node(value, None, None)
        else:
            if node.right is not None:
                self.__add_to(node.right, value)
            else:
                node.right = Node(value, None, None)
        node.unselect()

    def remove(self, value):
        if not self.is_empty():
            self._root = self.__remove_from(self.get_root(), value)
            self._size -= 1

    def __remove_from(self, node, value):
        node.select()
        self.suspend()
        result = node
        if value == node.value:
            if node.right is not None:
                min_node = self.__min_child_of(node.right)
                node.right = self.__remove_from(node, min_node.value)
                self.suspend()
                node.value = min_node.value
            else:
                result = node.left
        elif value < node.value:
            if node.left is not None:
                node.left = self.__remove_from(node.left, value)
        else:
            if node.right is not None:
                node.right = self.__remove_from(node.right, value)
        node.unselect()
        return result

    def __min_child_of(self, node):
        node.select()
        self.suspend()
        result = node
        if node.left is not None:
            result = self.__min_child_of(node.left)
        node.unselect()
        return result

    def get_root(self):
        return self._root
