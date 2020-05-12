class Node:
    def __init__(self, item, connected=None):
        self.next = connected
        self.item = item

    def __str__(self):
        return f"Node({self.item}, ...)"
