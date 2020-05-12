from modules.Containers.node import Node


class LinkedList:
    def __init__(self):
        self.head = None
        self.__length = 0

    def add(self, item):
        if self.__length:
            self.head = Node(item, self.head)
        else:
            self.head = Node(item)
        self.__length += 1

    def __len__(self):
        return self.__length

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            item = self._current.item
            self._current = self._current.next
            return item
