"""
Example for instagram-scraper
"""
from igramscraper.instagram import Instagram


def get_first_posts(num, username):

    # creating an instance of Instagram class
    instagram = Instagram()
    # gets posts of the given user
    media = instagram.get_medias(username, num)

    # returns captions of all the given media
    return [item.caption for item in media]


for item in get_first_posts(10, 'chorno_brova'):
    print(item)
