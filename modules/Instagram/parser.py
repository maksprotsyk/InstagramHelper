"""
Class for parsing of instagram profiles
"""
import re
from bs4 import BeautifulSoup
import requests



class HtmlParser:
    """
    Abstract class for parsing different web pages
    """
    def __init__(self, url: str) -> None:
        """
        Creates a parser with given url
        """
        self._url = url
        self._parser = None

    @property
    def parser(self) -> BeautifulSoup:
        """
        Returns a parser for the given page
        """
        if self._parser is None:
            html = requests\
                .get(self._url)\
                .text
            self._parser = BeautifulSoup(html, "html.parser")
        return self._parser

    @property
    def url(self) -> str:
        """
        Returns url of the page
        """
        return self._url

    @url.setter
    def url(self, new_url):
        """
        Sets new url and reinitializes the object
        """
        self.__init__(new_url)


class InstagramParser(HtmlParser):
    """
    Parser for instagram profiles
    """
    URL = ' http://www.instagram.com/{}'

    def __init__(self, username: str) -> None:
        """
        Initializes parser with given username
        """
        super().__init__(self.URL.format(username))
        self._data = None
        self._id = None
        self._username = username

    def _get_info(self) -> list:
        """
        Gets info about the user and saves it to a list
        """
        text = self.parser\
                   .find_all('script', type="text/javascript")[3]\
                   .text
        return re.findall(r'{"count":(.+?)[,}]', text)

    @staticmethod
    def convert_num(num: str) -> int:
        """
        Converts instagram number to the regular format
        """
        if 'm' in num:
            return int(float(num[:-1]) * 1000000)
        elif 'k' in num:
            return int(float(num[:-1]) * 1000)
        else:
            return int(num.replace(',', ''))

    def _get_data(self, index: int) -> int:
        """
        Gets data at the given index
        """
        if self._data is None:
            self._data = self._get_info()

        return self.convert_num(self._data[index])

    @property
    def followers(self) -> int:
        """
        Returns the umber of followers
        """
        return self._get_data(0)

    @property
    def following(self) -> int:
        """
        Returns the number of follows
        """
        return self._get_data(1)

    @property
    def posts(self) -> int:
        """
        Returns the number of posts
        """
        return self._get_data(4)

    @property
    def id(self) -> str:
        """
        Returns user id if it is not private
        """
        if self._id is None:
            text = self\
                .parser\
                .find_all('script', type="text/javascript")[3]\
                .text
            try:
                self._id = re.search(r'"owner":{"id":"(.+?)"[,}]',
                                     text)[1]
            except TypeError:
                pass

        return self._id

    @property
    def username(self) -> str:
        """
        Returns the username
        """
        return self._username

    @property
    def is_private(self) -> bool:
        """
        Checks if user is private
        """
        return self.id is None


if __name__ == '__main__':
    pass
