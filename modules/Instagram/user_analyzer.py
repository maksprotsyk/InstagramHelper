"""
Functions to analyze the inputted profiles and interact with user
"""
from modules.Containers.profilescontainer import ProfilesContainer

def analyze(usernames):
    """
    Analyzes the given usernames and returns a recommendation
    """
    container = ProfilesContainer()
    for profile in usernames:
        profile = profile.username
        if container.check_user(profile):
            container.get_posts(profile)
        print(profile)
    return container.collect_texts()

def get_first_post(username):
    instagram = Instagram()
    post = instagram.get_medias(username, 1)[0]
    return post.link


if __name__ == '__main__':
    print(get_first_post('chorno_brova'))
