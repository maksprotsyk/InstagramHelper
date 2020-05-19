"""
Implementation of the TextContainer
"""
import re
from nltk.stem import PorterStemmer
from modules.containers.multiset import Multiset


class TextContainer(Multiset):
    """
    Multiset that can process text
    """
    STOP_WORDS = []
    stemmer = PorterStemmer()

    @staticmethod
    def process_text(item: str) -> str:
        """
        Removes unnecessary symbols from the text
        and get stems of the words if it is possible
        """
        item = re.sub(r'([A-Z][a-z]+)', ' \\1', item)
        item = re.sub(r"\'", '', item)
        item = re.sub(r'\W|\d|_', ' ', item)
        item = re.sub(r'\s+', ' ', item)
        item = item.lower().strip()
        return ' '.join([TextContainer.stemmer.stem(word)
                         for word in item.split()
                         if item not in TextContainer.STOP_WORDS])

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
        return result


if __name__ == '__main__':
    pass
