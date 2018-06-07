class Recipe(object):
    name = ""
    country = ""
    course = ""
    author = ""
    views = int(0)
    ingredients = []
    directions = []
    id = int(0)

    # The class "constructor" - It's actually an initializer 
    def __init__(self, id, name, country, course, views, author, ingredients, directions):
        self.id = id
        self.name = name
        self.country = country
        self.course = course
        self.views = views
        self.author = author
        self.ingredients = ingredients
        self.directions = directions

def make_recipe(id, name, country, views, author, ingredients, directions):
    recipe = Recipe(id, name, country, views, author, ingredients, directions)
    return recipe
    
    