from instpector import Instpector, endpoints
from time import time
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
import random_user_agent.params as params
import re
from concurrent.futures import ProcessPoolExecutor as executor


def generate_user_agent():
    names = [params.SoftwareName.FIREFOX.value,
             params.SoftwareName.CHROME.value]
    system = [params.OperatingSystem.WINDOWS.value,
              params.OperatingSystem.LINUX.value,
              params.OperatingSystem.MAC_OS_X.value]
    randomiser = UserAgent(software_names=names,
                           operating_systems=system,
                           limit=100)
    return randomiser.get_random_user_agent()


class Analyzer:
    URL = "https://www.instagram.com/{}"

    def __init__(self):
        self.instpector = Instpector()
        self.profile = endpoints.factory.create("profile",
                                                self.instpector)
        self.following = endpoints.factory.create("following",
                                                  self.instpector)
        self.timeline = endpoints.factory.create("timeline",
                                                 self.instpector)
        self.username = None

    def login(self, username, password):
        self.instpector.login(username, password)
        self.username = username

    @staticmethod
    def get_parser(url):
        html = requests.get(url).text
        return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_info(parser):
        text = parser \
            .find_all('script', type="text/javascript")[3] \
            .text
        numbers = re.findall(r'{"count":(.+?)[,}]', text)
        info = {
            "followers": numbers[0],
            "following": numbers[1],
            "posts": numbers[4]
        }
        return {name: int(num.replace(',', ''))
                if 'm' not in num else int(float(num[:-1]) * 1000000)
                for name, num in info.items()}

    @staticmethod
    def process_user(user, followers=1000, posts=20):
        try:
            if not user.is_private:
                parser = Analyzer.get_parser(Analyzer
                                             .URL
                                             .format(user.username))
                info = Analyzer.get_info(parser)
                return info["followers"] > followers and info["posts"] > posts
            else:
                return False
        except ValueError:
            print(f'Unexpected ValueError: {user.username}')
            print(user)
            return False
        except AttributeError:
            print(f'Unexpected AttributeError: {user.username}')
            print(user)
            return False

    def get_followings(self, limit=100, amount=10):
        my_profile = self.profile.of_user('maxprotsyk')
        print(my_profile)
        users = self.following.of_user(my_profile.id)
        count1 = 0
        count2 = 0
        while count1 < limit and count2 < amount:
            count2 += 1
            user = users.__next__()
            if self.process_user(user):
                count1 += 1
                yield user

    def logout(self):
        self.instpector.logout()
        self.username = None
