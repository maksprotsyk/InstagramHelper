"""
Testing module for ProfilesContainer
(Not all methods are tested because instagram pages
are constantly changing and can't be tested)
"""
import unittest
from modules.containers.profiles_container import ProfilesContainer

class TestContainer(unittest.TestCase):
    """
    Testing class for ProfilesContainer
    """
    def setUp(self) -> None:
        """
        Sets up an empty container
        """
        self.container = ProfilesContainer()

    def test_check_user(self) -> None:
        """
        Tests check_user method
        """
        self.assertFalse(
            self.container.check_user('maxprotsyk')
        )
        self.assertFalse(
            self.container.check_user('lpml_elite')
        )
        self.assertTrue(
            self.container.check_user('chorno_brova')
        )

    def test_contains(self) -> None:
        """
        Tests __contains__ method
        """
        self.assertFalse('lol' in self.container)
        self.container._create('lol')
        self.assertTrue('lol' in self.container)


if __name__ == '__main__':
    unittest.main()