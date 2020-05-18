class Node:
    """
    Represents a node
    """
    def __init__(self, item, connected=None) -> None:
        """
        Initializes a node with given item and next node
        """
        self.next = connected
        self.item = item

    def __str__(self) -> str:
        """
        Returns string representation of the object
        """
        return f"Node({self.item}, ...)"
