from byotest import *
from recipemain import *

# delete the entire database and test
db_delete()
test_are_equal(user_count() == 0, True)
test_are_equal(recipe_count() == 0, True)
test_are_equal(ingredient_count() == 0, True)

# test the database functions for user
test_are_equal(user_register("mytestuser", "mypass"), True)
test_are_equal(user_authenticate("mybaduser", "mypass"), False)
test_are_equal(user_authenticate("mytestuser", "mypass"), True)
test_are_equal(user_authenticate("mytestuser", "badpass"), False)
user_delete("mytestuser")
test_are_equal(user_authenticate("mytestuser", "mypass"), False)


# Test insert recipe
author = "mytestuser"
user_register(author, "mypass")

# Make a recipe
name = "Pancakes"
country = "Greece"
course = "Breakfast"
# Each ingredient has a name, id and allergen

ingreds = []
ingredient1 = dict()
ingredient1['ingredient'] = 'flour'
ingredient1['amount'] = '200g'
ingredient1['allergen'] = 'wheat'
ingreds.append(ingredient1)
ingredient2 = {}
ingredient2['ingredient'] = 'egg'
ingredient2['amount'] = '1'
ingredient2['allergen'] = 'egg'
ingreds.append(ingredient2)
ingredient3 = {}
ingredient3['ingredient'] = 'milk'
ingredient3['amount'] = '200ml'
ingredient3['allergen'] = 'dairy'
ingreds.append(ingredient3)    

directions = []
direction1 = dict()
direction1['direction'] = "Sift the flour and salt into a mixing bowl and make a well in the centre. Crack the egg into the well; add the melted butter or oil and half the milk. Gradually draw the flour into the liquid by stirring all the time with a wooden spoon until all the flour has been incorporated and then beat well to make a smooth batter. Stir in the remaining milk. Alternatively, beat all the ingredients together for 1 minute in a blender or food processor. Leave to stand for about 30 minutes, stir again before using."
directions.append(direction1)
direction2 = dict()
direction2['direction'] = "To make the pancakes, heat a small heavy-based frying until very hot and then turn the heat down to medium. Lightly grease with oil and then ladle in enough batter to coat the base of the pan thinly (about 2 tablsp.), tilting the pan so the mixture spreads evenly. Cook over a moderate heat for 1-2 minutes or until the batter looks dry on the top and begins to brown at the edges. Flip the pancake over with a palette knife or fish slice and cook the second side."
directions.append(direction2)

recipeid = recipe_insert(name, author, country, course, ingreds, directions)

# Test everything was inserted in correctly
test_are_equal(user_count() == 1, True)
test_are_equal(recipe_count() == 1, True)
test_are_equal(ingredient_count() == 3, True)
test_are_equal(recipeid == 1, True)

# Retrieve the recipe from the database now
# should return a recipe object
recipe = recipe_get(recipeid)
test_are_equal(recipe.id == 1, True)
test_are_equal(recipe.name == "Pancakes", True)
test_are_equal(recipe.country == "Greece", True)
test_are_equal(recipe.course == "Breakfast", True)
ingrds = recipe.ingredients
test_are_equal(len(ingrds) == 3, True)

# Find flour
ingr = ""
for i in ingrds:
    if i.name == 'flour':
        ingr = i
        break

test_are_equal(not ingr == "", True)
test_are_equal(i.name == "flour", True)
test_are_equal(i.amount == "200g", True)
test_are_equal(i.allergen == "wheat", True)

# Find egg
ingr = ""
for i in ingrds:
    if i.name == 'egg':
        ingr = i
        break

test_are_equal(not ingr == "", True)
test_are_equal(i.name == "egg", True)
test_are_equal(i.amount == "1", True)
test_are_equal(i.allergen == "egg", True)

# Find milk
ingr = ""
for i in ingrds:
    if i.name == 'milk':
        ingr = i
        break

test_are_equal(not ingr == "", True)
test_are_equal(i.name == "milk", True)
test_are_equal(i.amount == "200ml", True)
test_are_equal(i.allergen == "dairy", True)
