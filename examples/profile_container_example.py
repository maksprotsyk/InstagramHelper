"""
Example for ProfilesContainer
"""
from modules.containers.profiles_container import ProfilesContainer

USER1 = 'toyota'

USER2 = 'lamborghini'


CONTAINER = ProfilesContainer()

CONTAINER.get_posts(USER1)
CONTAINER.get_posts(USER2)

print(CONTAINER.collect_texts())
