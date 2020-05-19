"""
Implementation of the Multiset
"""
from modules.containers.node import Node


class Multiset:
    """
    Unordered sequence with repeating items
    """
    def __init__(self) -> None:
        """
        Initializes an empty Multiset
        """
        self.head = None
        self.__length = 0
        self._current = self.head

    def add(self, item: object) -> None:
        """
        Adds an item to the multiset
        """
        if self.__length:
            self.head = Node(item, self.head)
        else:
            self.head = Node(item)
        self.__length += 1

    def remove(self, item: object) -> None:
        """
        Removes the first item equal to the given
        (does nothing if multiset doesn't contain it)
        """
        node = self.head
        if node is not None:
            if node.item == item:
                self.head = self.head.next
                self.__length -= 1
            else:
                while node.next is not None and node.next.item != item:
                    node = node.next
                if node.next is not None:
                    node.next = node.next.next
                    self.__length -= 1

    def __len__(self) -> int:
        """
        Returns the length of the multiset
        """
        return self.__length

    def __iter__(self):
        """
        Allows to iter through the multiset
        """
        self._current = self.head
        return self

    def __next__(self) -> object:
        """
        Returns next item (for the iter method)
        """
        if self._current is None:
            raise StopIteration
        item = self._current.item
        self._current = self._current.next
        return item

    def __contains__(self, item) -> bool:
        """
        Checks if item is present in the multiset
        """
        for value in self:
            if value == item:
                return True
        return False

    def __str__(self) -> str:
        """
        Represents multiset in string format
        """
        string = ""
        for item in self:
            string += f"{item} -> "
        return string + "..."


if __name__ == '__main__':
    pass
