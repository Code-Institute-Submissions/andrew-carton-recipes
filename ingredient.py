class Ingredient(object):
    name = ""
    allergen = ""
    amount = ""

    def __init__(self, name, allergen, amount):
        self.name = name
        self.allergen = allergen
        self.amount = amount

