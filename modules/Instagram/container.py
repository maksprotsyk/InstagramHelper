from types import GeneratorType
from modules.Containers.circledlist import CircledList
from modules.Containers.linkedlist import LinkedList


class BadGenerator(Exception):
    pass


class GeneratorContainer:
    def __init__(self):
        self.generators = CircledList()
        self.items = LinkedList()

    def add_generator(self, generator):
        if not isinstance(generator, GeneratorType):
            raise BadGenerator('Can add only Generators')
        else:
            self.generators.add(generator)

    def add_item(self, item):
        self.items.add(item)

    def generate_item(self):
        for i in range(len(self.generators)):
            try:
                self.add_item(self.generators.get().__next__())
            except StopIteration:
                self.generators.remove()
            else:
                self.generators.forward()
                break

    def __len__(self):
        return len(self.items)

    def is_finished(self):
        return len(self.generators) == 0

    def save_items(self, limit=10):
        i = 0
        while i < limit and len(self.generators):
            self.generate_item()
            i += 1

    def __str__(self):
        return str(self.items)

    def __iter__(self):
        return iter(self.items)
