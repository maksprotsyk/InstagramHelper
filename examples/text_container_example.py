"""
Example for TextContainer
"""
from modules.containers.text_container import TextContainer


text1 = ('Room for the whole gang. #TOYOTA'
         ' #Tundra #SUV #4X4 #4WD #Offroad'
         ' #ToyotaNation #ToyotaFamily #CarsOfInstagram'
         ' #CarOfTheDay #InstaAuto #AutoNation #Drive '
         '#Ride #TheGreatOutdoors #Adventure #EnjoyNature')


text2 = ('The beast in the forest. #TOYOTA #Tundr'
         'a #Pickup #4X4 #4WD #Offroad #ToyotaNation'
         ' #ToyotaFamily #CarsOfInstagram #CarOfTheDay'
         ' #InstaAuto #AutoNation #Drive #Ride #TheGreatOutdoors'
         ' #Adventure #EnjoyNature')


container = TextContainer()

container.add(text1)
container.add(text2)

container.process_container()

print(container.join_with(' '))
