"""
Implementation of the ProfilesContainer
"""
from modules.Containers.textcontainer import TextContainer
from modules.Instagram.parser import InstagramParser
from igramscraper.instagram import Instagram


class ProfilesContainer:
    """
    Special object for containing profiles
    """
    def __init__(self) -> None:
        """
        Initializes an empty container
        """
        self.profiles = dict()
        self.controller = Instagram()

    def __len__(self) -> int:
        """
        Returns length of the container
        """
        return len(self.profiles)

    def _create(self, username: str) -> None:
        """
        Creates a user with no posts
        """
        self.profiles[username] = self.profiles.get(username, None)

    def __contains__(self, username: str) -> bool:
        """
        Checks if user is created in the container
        """
        return username in self.profiles

    def get_posts(self, username: str) -> list:
        """
        Gets first 5 posts of the user if they weren't
        already saved (also created the user if it is not
        in the container)
        """
        self._create(username)
        if self.profiles[username] is None:
            self.profiles[username] = self.controller.get_medias(username, 5)
        return self.profiles[username]

    def collect_texts(self) -> str:
        """
        Collects the captions of all posts
        and processes them with TextContainer
        """
        texts = TextContainer()
        for posts in self.profiles.values():
            for post in posts:
                if post.caption is not None:
                    texts.add(post.caption)
        texts.process_container()
        return texts.join_with(' ')

    @staticmethod
    def check_user(username: str) -> bool:
        """
        Checks if user has at least 1000 followers,
        less than 1000 follows and is not private
        """
        parser = InstagramParser(username)
        return (not parser.is_private and
                parser.followers > 1000 > parser.following)


if __name__ == '__main__':
    pass
