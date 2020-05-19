"""
Functions to analyze the inputted profiles and interact with user
"""
from sklearn.pipeline import Pipeline
from pandas import DataFrame
from igramscraper.instagram import Instagram,\
                                   InstagramNotFoundException,\
                                   InstagramException
from modules.containers.profiles_container import ProfilesContainer
from modules.containers.text_container import TextContainer

def analyze(usernames: list, model: Pipeline,
            dataframe: DataFrame, stop_words: list,
            length=30) -> list:
    """
    Analyzes the given usernames and returns a recommendation
    """
    TextContainer.STOP_WORDS = stop_words
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
        return dataframe[
            dataframe['cluster'] == cluster
            ]['following'].values
    return None


def get_first_post(username: str) -> str:
    """
    Gets link to the first users post
    """
    try:
        instagram = Instagram()
        post = instagram.get_medias(username, 1)[0]
        return post.link
    except (InstagramException,
            InstagramNotFoundException,
            IndexError):
        return ''


if __name__ == '__main__':
    pass
