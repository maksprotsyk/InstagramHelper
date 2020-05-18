"""
Example for ProfilesContainer
"""
from modules.Containers.profilescontainer import ProfilesContainer

user1 = 'toyota'

user2 = 'lamborghini'


container = ProfilesContainer()

container.get_posts(user1)
container.get_posts(user2)

print(container.collect_texts())
