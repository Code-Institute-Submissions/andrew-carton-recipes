class Ingredient(object):
    name = ""
    allergen = ""
    amount = ""
    

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, allergen, amount):
        self.name = name
        self.allergen = allergen
        self.amount = amount

def make_ingredient(name, allergen, amount):
    i = Ingredient(name, allergen, amount)
    return i
    
    
    
    