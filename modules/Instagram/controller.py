from instpector import Instpector, endpoints


class AccountController:
    def __init__(self, username, password):
        self._account = Instpector()
        self._account.login(username, password)
        self._username = username
        self.profile = endpoints.factory.create("profile",
                                                self._account)
        self.following = endpoints.factory.create("following",
                                                  self._account)
        self.timeline = endpoints.factory.create("timeline",
                                                 self._account)

    def get_profile(self, username):
        return self.profile.of_user(username)

    def exit(self):
        self._account.logout()


class InstagramProfile:
    def __init__(self, username, controller, user=None, profile=None):
        self._username = username
        self.controller = controller
        self._user = user
        self._profile = profile
        self.posts = []

    def _get_profile_info(self, attribute):
        if self._profile is None:
            self._profile = self \
                .controller \
                .get_profile(self._username)
        return self._profile.__getattribute__(attribute)

    def _get_user_info(self, attribute):
        if self._user is not None:
            return self._user.__getattribute__(attribute)
        else:
            return self._get_profile_info(attribute)

    @property
    def id(self):
        return self._get_user_info('id')

    @property
    def is_private(self):
        return self._get_user_info('is_private')

    @property
    def biography(self):
        return self._get_profile_info('is_private')

    @property
    def followers_count(self):
        return self._get_profile_info('followers_count')

    @property
    def following_count(self):
        return self._get_profile_info('following_count')
