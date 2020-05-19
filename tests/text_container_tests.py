"""
Testing module for TextContainer
(Tests new methods and add method of the multiset)
"""
import unittest
from modules.containers.text_container import TextContainer


class TextTest(unittest.TestCase):
    """
    Class for tesing TextContainer
    """
    def setUp(self) -> None:
        """
        Sets up some strings and an empty TextContainer
        """
        self.text1 = '1221313zdmdsk'
        self.text2 = 'fsls,sfsf_   f'
        self.text3 = 'activity'
        self.container = TextContainer()

    def test_process_text(self) -> None:
        """
        Tests process_text method
        """
        self.assertEqual(
            self.container.process_text(self.text1), 'zdmdsk'
        )
        self.assertEqual(
            self.container.process_text(self.text2), 'fsl sfsf f'
        )
        self.assertEqual(
            self.container.process_text(self.text3), 'activ'
        )

    def test_add(self) -> None:
        """
        Tests add method
        """
        self.container.add(self.text1)
        self.container.add(self.text2)
        self.assertEqual(len(self.container), 2)
        self.assertTrue(self.text1 in self.container)
        self.assertTrue(self.text2 in self.container)

    def test_process_container(self) -> None:
        """
        Tests process_container method
        """
        self.container.add(self.text1)
        self.container.add(self.text2)
        self.container.add(self.text3)
        self.container.process_container()
        self.assertEqual(self.container.join_with(' '),
                         'activ fsl sfsf f zdmdsk')

if __name__ == '__main__':
    unittest.main()
