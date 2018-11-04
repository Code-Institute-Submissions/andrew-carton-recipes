""" 
    Ingredient class:

    Encapsulates an ingredient which is a name, allergen and amount.

"""
class Ingredient():

    # Constructor
    def __init__(self, name, allergen, amount):
        self.name = name
        self.allergen = allergen
        self.amount = amount

