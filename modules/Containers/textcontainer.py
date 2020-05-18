from modules.Containers.multiset import Multiset
import re
from nltk.stem import PorterStemmer

class TextContainer(Multiset):
    @staticmethod
    def process_text(item):
        item = re.sub('\W|\d|_', ' ', item)
        item = re.sub('\s+', ' ', item)
        return item.lower().strip()

    def process_container(self):
        node = self.head
        while node is not None:
            node.item = self.process_text(node.item)
            node = node.next

    def join_with(self, string):
        result = ''
        if len(self) != 0:
            for item in self:
                result  += item
                result += string
            return result[:-len(string)]
        else:
            return result



x = TextContainer()
x.add('dlmldld')
x.add('ada,lad,')

x.process_container()
print(x.join_with(' '))