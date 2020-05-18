"""
Implementation of the TextContainer
"""
import re
from modules.Containers.multiset import Multiset
# from nltk.stem import PorterStemmer


class TextContainer(Multiset):
    """
    Multiset that can process text
    """

    @staticmethod
    def process_text(item: str) -> str:
        """
        Removes unnecessary symbols from the text
        and get stems of the words if it is possible
        """
        item = re.sub('\W|\d|_', ' ', item)
        item = re.sub('\s+', ' ', item)
        return item.lower().strip()

    def process_container(self) -> None:
        """
        Processes all the texts in the container
        """
        node = self.head
        while node is not None:
            node.item = self.process_text(node.item)
            node = node.next

    def join_with(self, string: str) -> str:
        """
        Joins all the texts with given string
        """
        result = ''
        if self.head is not None:
            for item in self:
                result += item
                result += string
            return result[:-len(string)]
        else:
            return result


if __name__ == '__main__':
    pass
