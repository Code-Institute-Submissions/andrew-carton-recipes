from recipedatabase import RecipeDatabase
import unittest
import sys
sys.path.append('../')


class RecipeTest(unittest.TestCase):

    # Set up the database and get a connection
    @classmethod
    def setUpClass(self):
        self.database = RecipeDatabase("testing.db")
        self.conn = self.database.engine.connect()
        # delete the entire database and test
        self.database.db_delete(self.conn)

    # Close the database connection on tear down
    @classmethod
    def tearDownClass(self):
        self.conn.close()

    def test_emptydb(self):
        self.assertEqual(self.database.user_count(self.conn) == 0, True)
        self.assertEqual(self.database.recipe_count(self.conn) == 0, True)
        self.assertEqual(self.database.ingredient_count(self.conn) == 0, True)

    def test_database_user(self):
        # test the database functions for user
        self.assertEqual(self.database.user_register("mytestuser",
                                                     "mypass", self.conn),
                         True)
        self.assertEqual(self.database.user_authenticate(
            "mybaduser", "mypass", self.conn), False)
        self.assertEqual(self.database.user_authenticate(
            "mytestuser", "mypass", self.conn), True)
        self.assertEqual(self.database.user_authenticate(
            "mytestuser", "badpass", self.conn), False)
        self.database.user_delete("mytestuser", self.conn)
        self.assertEqual(self.database.user_authenticate(
            "mytestuser", "mypass", self.conn), False)

    def test_insert_recipe(self):
        # Test insert recipe
        author = "mytestuser"
        self.database.user_register(author, "mypass", self.conn)
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
        direction1['direction'] = "Sift the flour and salt into a mixing bowl \
        and make a well in the centre. Crack the egg into the well; add the \
        melted butter or oil and half the milk. Gradually draw the flour into \
        the liquid by stirring all the time with a wooden spoon until all the \
        flour has been incorporated and then beat well to make a smooth \
        batter. Stir in the remaining milk. Alternatively, beat all \
         the ingredients together for 1 minute in a  blender or food \
         processor. Leave to stand for about 30 minutes, stir again \
         before using."
        directions.append(direction1)
        direction2 = dict()
        direction2[
            'direction'] = "To make the pancakes, heat a small \
            heavy-based frying until very hot and then turn the \
            heat down to medium. Lightly grease with oil and then \
            ladle in enough batter to coat the base of the pan \
            thinly (about 2 tablsp.), tilting the pan so the \
            mixture spreads evenly. Cook over a moderate heat \
            for 1-2 minutes or until the batter looks dry on \
            the top and begins to brown at the edges. Flip the \
            pancake over with a palette knife or fish slice and \
            cook the second side."
        directions.append(direction2)

        recipeid = self.database.recipe_insert(
            name, author, country, course, ingreds, directions, "", self.conn)

        # Test everything was inserted in correctly
        self.assertEqual(self.database.user_count(self.conn) == 1, True)
        self.assertEqual(self.database.recipe_count(self.conn) == 1, True)
        self.assertEqual(self.database.ingredient_count(self.conn) == 3, True)
        self.assertEqual(recipeid == 1, True)

        # Retrieve the recipe from the database now
        # should return a recipe object
        recipe = self.database.recipe_get(recipeid, self.conn)
        self.assertEqual(recipe.id == 1, True)
        self.assertEqual(recipe.name == "Pancakes", True)
        self.assertEqual(recipe.country == "Greece", True)
        self.assertEqual(recipe.course == "Breakfast", True)
        ingrds = recipe.ingredients
        self.assertEqual(len(ingrds) == 3, True)

        # Find flour
        ingr = ""
        for i in ingrds:
            if i.name == 'flour':
                ingr = i
                break

        self.assertEqual(not ingr == "", True)
        self.assertEqual(i.name == "flour", True)
        self.assertEqual(i.amount == "200g", True)
        self.assertEqual(i.allergen == "wheat", True)

        # Find egg
        ingr = ""
        for i in ingrds:
            if i.name == 'egg':
                ingr = i
                break

        self.assertEqual(not ingr == "", True)
        self.assertEqual(i.name == "egg", True)
        self.assertEqual(i.amount == "1", True)
        self.assertEqual(i.allergen == "egg", True)

        # Find milk
        ingr = ""
        for i in ingrds:
            if i.name == 'milk':
                ingr = i
                break

        self.assertEqual(not ingr == "", True)
        self.assertEqual(i.name == "milk", True)
        self.assertEqual(i.amount == "200ml", True)
        self.assertEqual(i.allergen == "dairy", True)


if __name__ == '__main__':
    unittest.main()
