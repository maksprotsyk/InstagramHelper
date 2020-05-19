"""
Testing module for Multiset
"""
import unittest
from modules.containers.multiset import Multiset


class TestSet(unittest.TestCase):
    """
    Testing class for Multiset
    """
    def setUp(self) -> None:
        """
        Sets up an empty multiset
        """
        self.set = Multiset()

    def test_contains(self) -> None:
        """
        Checks __contains__ method
        """
        self.set.add(2)
        self.assertTrue(2 in self.set)

    def test_add(self) -> None:
        """
        Checks add method
        """
        self.set.add(1)
        self.set.add(2)
        self.set.add(3)
        self.assertEqual(len(self.set), 3)
        self.assertTrue(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertTrue(3 in self.set)

    def test_remove(self) -> None:
        """
        Checks remove method
        """
        self.set.add(1)
        self.set.add(2)
        self.set.remove(1)
        self.set.remove(3)
        self.assertFalse(1 in self.set)
        self.assertTrue(2 in self.set)
        self.assertTrue(len(self.set), 1)

    def test_next(self) -> None:
        """
        Checks __next__ method
        """
        self.set.add(1)
        self.set.add(2)
        self.set.__iter__()
        self.assertEqual(self.set.__next__(), 2)
        self.assertEqual(self.set.__next__(), 1)

    def test_str(self) -> None:
        """
        Tests __str__ method
        """
        self.set.add(1)
        self.set.add(2)
        self.assertEqual(str(self.set), '2 -> 1 -> ...')


if __name__ == '__main__':
    unittest.main()
