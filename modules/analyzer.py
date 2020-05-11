from instpector import Instpector, endpoints
from time import time
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
import random_user_agent.params as params
import re
import multiprocessing


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
        self.profiles = []

    def login(self, username, password):
        self.instpector.login(username, password)
        self.username = username

    @staticmethod
    def get_parser(url):
        html = requests.get(url).text
        return BeautifulSoup(html, "html.parser")

    @staticmethod
    def get_info(parser):
        text = parser\
            .find_all('script', type="text/javascript")[3]\
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

    def process_user(self, user, followers=1000, posts=20):
        try:
            if not user.is_private:
                parser = Analyzer.get_parser(Analyzer
                                             .URL
                                             .format(user.username))
                info = Analyzer.get_info(parser)
                if info["followers"] > followers and info["posts"] > posts:
                    self.profiles.append(user)
                    print(user)
        except ValueError:
            print(f'Unexpected ValueError: {user.username}')
            print(user)
        except AttributeError:
            print(f'Unexpected AttributeError: {user.username}')
            print(user)

    def get_followings(self, limit=100, amount=10):
        my_profile = self.profile.of_user('maxprotsyk')
        users = self.following.of_user(my_profile.id)
        count = 0
        while count < amount and len(self.profiles) < limit:
            processes = []
            for i in range(2):
                count += 1
                user = users.__next__()
                p = multiprocessing.Process(target=self.process_user,
                                            args=(user,))
                processes.append(p)
                p.start()

            for process in processes:
                process.join()

    def logout(self):
        self.instpector.logout()
        self.username = None
