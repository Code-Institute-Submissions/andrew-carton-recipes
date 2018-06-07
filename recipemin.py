class RecipeMin(object):
    name = ""
    id = int(0)

     
    def __init__(self, id, name):
        self.id = id
        self.name = name
        

def make_recipe(id, name, ):
    recipe = RecipeMin(id, name)
    return recipe
    
    