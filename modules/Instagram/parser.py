from bs4 import BeautifulSoup
import requests
import re

class InvalidURL(Exception):
    pass

class HtmlParser:
    def __init__(self, url):
        self._url = url
        self._parser = None

    @property
    def parser(self):
        if self._parser is None:
            html = requests\
                .get(self._url)\
                .text
            self._parser = BeautifulSoup(html, "html.parser")
        return self._parser

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self.__init__(new_url)


class InstagramParser(HtmlParser):
    URL = ' http://www.instagram.com/{}'

    def __init__(self, username):
        super().__init__(self.URL.format(username))
        self._data = None
        self._id = None
        self._username = username

    def get_info(self):
        text = self.parser\
               .find_all('script', type="text/javascript")[3]\
               .text
        return re.findall(r'{"count":(.+?)[,}]', text)

    @staticmethod
    def convert_num(num):
        if 'm' in num:
            return int(float(num[:-1]) * 1000000)
        elif 'k' in num:
            return int(float(num[:-1]) * 1000)
        else:
            return int(num.replace(',', ''))

    def _get_data(self, index):
        if self._data is None:
            self._data = self.get_info()

        return self.convert_num(self._data[index])

    @property
    def followers(self):
        return self._get_data(0)

    @property
    def following(self):
        return self._get_data(1)

    @property
    def posts(self):
        return self._get_data(4)

    @property
    def id(self):
        if self._id is None:
            text = self\
                .parser\
                .find_all('script', type="text/javascript")[3]\
                .text
            try:
                self._id = re.search(r'"owner":{"id":"(.+?)"[,}]', text)[1]
            except TypeError:
                self._id = None
            else:
                return self._id

    @property
    def username(self):
        return self._username

    @property
    def is_private(self):
        return self.id is None

