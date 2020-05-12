from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import re


class InvalidURL(Exception):
    pass


class HtmlParser:
    def __init__(self, url):
        self._url = url
        self._parser = self.get_parser()

    def get_parser(self):
        html = requests\
            .get(self._url, {'User-agent': UserAgent().chrome})\
            .text
        return BeautifulSoup(html, "html.parser")

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

    def get_info(self):
        text = self._parser\
               .find_all('script', type="text/javascript")[3]\
               .text
        return re.findall(r'{"count":(.+?)[,}]', text)

    @staticmethod
    def convert_num(num):
        return (int(num.replace(',', '')
                if 'm' not in num
                else int(float(num[:-1]) * 1000000)))

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
