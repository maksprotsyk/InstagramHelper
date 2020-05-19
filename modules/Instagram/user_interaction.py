"""
Functions to analyze the inputted profiles and interact with user
"""
from sklearn.pipeline import Pipeline
from pandas import DataFrame
from igramscraper.instagram import Instagram
from modules.Containers.profiles_container import ProfilesContainer


def analyze(usernames: list, model: Pipeline,
            df: DataFrame, length=30) -> list:
    """
    Analyzes the given usernames and returns a recommendation
    """
    container = ProfilesContainer()
    for profile in usernames:
        if container.check_user(profile):
            container.get_posts(profile)
    text = container.collect_texts()
    if len(text) > length:
        vector = model.named_steps['vectorizer']\
                      .transform([text])\
                      .toarray()
        cluster = model.named_steps['clustering']\
                       .predict(vector)[0]
        return df[df['cluster'] == cluster]['following'].values
    else:
        return None


def get_first_post(username: str) -> str:
    """
    Gets link to the first users post
    """
    instagram = Instagram()
    post = instagram.get_medias(username, 1)[0]
    return post.link


if __name__ == '__main__':
    pass
