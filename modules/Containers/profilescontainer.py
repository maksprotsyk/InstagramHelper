from modules.Containers.textcontainer import TextContainer
from modules.Instagram.parser import InstagramParser
from insta.igramscraper.instagram import Instagram

class UserError(Exception):
    pass


class ProfilesContainer:
    def __init__(self):
        self.profiles = dict()
        self.controller = Instagram()

    def _create(self, username):
        self.profiles[username] = self.profiles.get(username, None)

    def __contains__(self, username):
        return username in self.profiles

    def get_posts(self, username):
        self._create(username)
        if self.profiles[username] is None:
            self.profiles[username] = self.controller.get_medias(username, 5)
        return self.profiles[username]


    def collect_texts(self):
        texts = TextContainer()
        for posts in self.profiles.values():
            for post in posts:
                if post.caption is not None:
                    texts.add(post.caption)

        texts.process_container()
        return texts.join_with(' ')

    @staticmethod
    def check_user(username):
        parser = InstagramParser(username)
        return (not parser.is_private and
                parser.followers > 1000 and
                parser.following < 1000)
