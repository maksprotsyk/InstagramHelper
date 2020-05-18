from modules.Containers.node import Node


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

    def add(self, item) -> None:
        """
        Adds an item to the multiset
        """
        if self.__length:
            self.head = Node(item, self.head)
        else:
            self.head = Node(item)
        self.__length += 1

    def remove(self, item) -> None:
        """
        Removes the first item equal to the given
        (does nothing if multiset doesn't contain it)
        """
        node = self.head
        while node is not None and node.item != item:
            node = node.next
        if node.item == item:
            node

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

    def __next__(self):
        """
        Returns next item (for the iter method)
        """
        if self._current is None:
            raise StopIteration
        else:
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
        else:
            return False

    def __str__(self) -> str:
        """
        Represents multiset in string format
        """
        string = ""
        for item in self:
            string += f"{item} -> "
        return string + "..."
