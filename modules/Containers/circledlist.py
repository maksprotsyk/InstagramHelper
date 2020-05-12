from modules.Containers.node import Node


class EmptyList(Exception):
    pass


class CircledList:
    def __init__(self):
        self.current = None
        self.previous = None
        self.__length = 0

    def add(self, item):
        if self.current is None:
            self.current = Node(item)
            self.previous = self.current
            self.previous.next = self.current
            self.__length += 1
        else:
            self.previous.next = Node(item, self.current)
            self.previous = self.previous.next
            self.__length += 1

    def __len__(self):
        return self.__length

    def is_empty(self):
        return self.current is None

    def remove(self):
        if self.__length == 0:
            raise EmptyList('CircledList is already empty')
        elif self.__length == 1:
            self.current = None
            self.previous = None
            self.__length = 0
        else:
            self.current = self.current.next
            self.previous.next = self.current
            self.__length -= 1

    def get(self):
        if self.__length:
            return self.current.item
        else:
            raise EmptyList("List is empty")

    def forward(self):
        self.previous = self.previous.next
        self.current = self.current.next

    def __str__(self):
        string = "... -> "
        for i in range(len(self)):
            string += f"{self.get()} -> "
            self.forward()
        return string + "..."
