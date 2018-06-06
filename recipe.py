class Recipe(object):
    name = ""
    country = ""
    course = ""
    views = int(0)
    ingredients = []
    directions = []
    id = int(0)

    # The class "constructor" - It's actually an initializer 
    def __init__(self, id, name, country, course, views, ingredients, directions):
        self.id = id
        self.name = name
        self.country = country
        self.course = course
        self.views = views
        self.ingredients = ingredients
        self.directions = directions

def make_recipe(id, name, country, views, ingredients, directions):
    recipe = Recipe(id, name, country, views, ingredients, directions)
    return recipe
    
    