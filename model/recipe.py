"""

    Recipe class:

    Encapsulates a recipe.

    It includes an id, name, country, course (e.g. main or starter), 
    number of views, the author,  the list of ingredients 
    (See Ingredient class), the list of directions (See Directions Class)
    and the image.

"""


class Recipe():

    # Constructor
    def __init__(self, id, name, country, course, views, author, 
                 ingredients, image, directions):
        self.id = id
        self.name = name
        self.country = country
        self.course = course
        self.views = views
        self.author = author
        self.ingredients = ingredients
        self.directions = directions
        self.image = image
