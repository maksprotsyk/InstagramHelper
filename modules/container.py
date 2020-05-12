from types import GeneratorType


class Node:
    def __init__(self, item, connected=None):
        self.next = connected
        self.item = item

    def __str__(self):
        return f"Node({self.item}, ...)"


class BadGenerator(Exception):
    pass


class GeneratorContainer:
    def __init__(self):
        self._previous = None
        self._current = None
        self._generator_length = 0
        self._items = None
        self._item_length = 0

    def add_generator(self, generator):
        '''
        if not isinstance(generator, GeneratorType):
            raise BadGenerator('Can add only Generators')
        else:
        '''
        if self._generator_length == 0:
            self._current = Node(generator)
            self._previous = self._current
            self._previous.next = self._current
            self._generator_length += 1
        else:
            self._previous.next = Node(generator,
                                       self._current)
            self._previous = self._previous.next
            self._generator_length += 1

    def add_item(self, item):
        if self._items is None:
            self._items = Node(item)
        else:
            self._items = Node(item, self._items)
        self._item_length += 1

    def generate_item(self):
        for i in range(self._generator_length):
            try:
                self.add_item(self._current.item.__next__())
            except StopIteration:
                if self._generator_length > 1:
                    self._current = self._current.next
                    self._previous.next = self._current
                    self._generator_length -= 1
                else:
                    self._current = None
                    self._previous = None
                    self._generator_length = 0
            else:
                self._current = self._current.next
                self._previous = self._previous.next
                break

    def __len__(self):
        return self._item_length

    def isempty(self):
        return self._current is None

    def save_items(limit=10):
        i = 0
        while i < limit and self._generator_length > 0:
            self.generate_item()

    def __str__(self):
        string = ""
        head = self._items
        for i in range(self._item_length):
            string += f"{head.item} -> "
            head = head.next
        return string[:-4]
