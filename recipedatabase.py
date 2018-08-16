
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.sql import select, func
from classes.direction import Direction
from classes.ingredient import Ingredient
from classes.recipe import Recipe


class RecipeDatabase:
    def __init__(self, dbname):

        self.engine = create_engine('sqlite:///' + dbname, echo=False)
        metadata = MetaData()

        self.users = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('password', String)
        )

        self.recipes = Table('recipes', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String, nullable=False),
                        Column('country', String, nullable=False),
                        Column('course', String, nullable=False),
                        Column('image', String, nullable=False),
                        Column('views', Integer, nullable=False),
                        Column('user_id', None, ForeignKey('users.id'))
        )

        self.ingredients=Table('ingredients', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('allergen', String),
        )

        self.ingredients_list=Table('ingredients_list', metadata,
                                Column('recipe_id', None, ForeignKey('recipes.id')),
                                Column('ingredient_id', None,
                                        ForeignKey('ingredients.id')),
                                Column('quantity', String, nullable=False)
        )

        self.directions_list=Table('directions_list', metadata,
                                Column('recipe_id', None, ForeignKey('recipes.id')),
                                Column('text', String, nullable=False),
                                Column('number', Integer, nullable=False)
        )

        metadata.create_all(self.engine)

    def user_register(self, uname, password, connection):
        s = select([self.users]).where(self.users.c.name == uname)
        result = connection.execute(s)
        rows = result.fetchall()
        amount = len(rows)
        if amount > 0:
            return False
        else:
            connection = self.engine.connect()
            ins = self.users.insert().values(name=uname, password=password)
            connection.execute(ins)
            return True


    # authenticate a user against a password
    # return False if failed
    def user_authenticate(self, uname, password, connection):
        s = select([self.users]).where((self.users.c.name == uname)
                                & (self.users.c.password == password))
        result = connection.execute(s)
        rows = result.fetchall()
        amount = len(rows)
        if amount > 0:
            return True
        return False


    # delete a user
    def user_delete(self, uname, connection):
        res = self.users.delete(self.users.c.name == uname)
        connection.execute(res)


    # return amount of users
    def user_count(self, connection):
        res = select([self.users])
        result = connection.execute(res)
        rows = result.fetchall()
        return len(rows)


    # return amount of recipes
    def recipe_count(self, connection):
        res = select([self.recipes])
        result = connection.execute(res)
        rows = result.fetchall()
        return len(rows)


    # return amount of ingredients
    def ingredient_count(self, connection):
        res = select([self.ingredients])
        result = connection.execute(res)
        rows = result.fetchall()
        return len(rows)


    # delete contents of database
    def db_delete(self, connection):
        res = select([self.recipes])
        total = connection.execute(res)
        for x in total:
            self.recipe_delete(x.id, connection)

        res = select([self.users])
        total = connection.execute(res)
        for x in total:
            y = self.users.delete().where(self.users.c.id == x.id)
            connection.execute(y)


    # delete all ingredients associated with a recipe (given an id of recipe)
    def ingredients_delete(self, recipeid, connection):
        res = select([self.ingredients_list]).where(
            self.ingredients_list.c.recipe_id == recipeid)
        total = connection.execute(res)
        for x in total:
            res2 = self.ingredients.delete().where(self.ingredients.c.id == x.ingredient_id)
            connection.execute(res2)
        y = self.ingredients_list.delete().where(self.ingredients_list.c.recipe_id == recipeid)
        connection.execute(y)


    # delete all directions associated with a recipe (given an id of recipe)
    def directions_delete(self, recipeid, connection):
        res = select([self.directions_list])
        connection.execute(res)
        y = self.directions_list.delete().where(self.directions_list.c.recipe_id == recipeid)
        connection.execute(y)


    # deletes a recipe and all it's data from the db
    def recipe_delete(self, id, connection):
        self.ingredients_delete(id, connection)
        self.directions_delete(id, connection)
        res = self.recipes.delete().where(self.recipes.c.id == id)
        connection.execute(res)


    # insert an ingredient into a recipe given the recipe id and an ingredient
    def ingredient_insert(self, recipeid, ingredient, conn):

        s = select([self.recipes]).where(self.recipes.c.id == recipeid)
        result = conn.execute(s)
        one_row = result.fetchone()
        ins = self.ingredients.insert().values(
            name=ingredient['ingredient'], allergen=ingredient['allergen'])
        res = conn.execute(ins)
        ingredientpkey = res.inserted_primary_key
        ins = self.ingredients_list.insert().values(recipe_id=one_row.id,
                                            ingredient_id=ingredientpkey[0], quantity=ingredient['amount'])
        res = conn.execute(ins)


    # insert a direction into a recipe given the recipe id and a direction and a number for the direction number
    def direction_insert(self, recipeid, direction, num, conn):
        s = select([self.recipes]).where(self.recipes.c.id == recipeid)
        result = conn.execute(s)
        one_row = result.fetchone()
        ins = self.directions_list.insert().values(
            recipe_id=one_row.id, text=direction['direction'], number=num)
        conn.execute(ins)


    # insert a recipe
    def recipe_insert(self, name, author, country, course, ingreds, directions, image, connection):
        idx = 1
        s = select([self.users]).where(self.users.c.name == author)
        result = connection.execute(s)

        idx = result.fetchone().id
        if image == "":
            image = "default.png"

        ins = self.recipes.insert().values(name=name, country=country, course=course,
                                    image=image, views=int(0), user_id=idx)
        res = connection.execute(ins)
        recipepkey = res.inserted_primary_key
        num = int(0)

        for i in ingreds:
            self.ingredient_insert(recipepkey[0], i, connection)

        for i in directions:
            self.direction_insert(recipepkey[0], i, num, connection)
            num = num + 1

        return recipepkey[0]


# retrieve a recipe (as a Recipe object)
    def recipe_get(self, idx, conn):
        selrecipes = select([self.recipes]).where(self.recipes.c.id == idx)
        recipesresult = conn.execute(selrecipes)

        recipex = ""

        for recipesrow in recipesresult:
            selusers = select([self.users]).where(self.users.c.id == recipesrow.user_id)
            usersresult = conn.execute(selusers)
            author = usersresult.fetchone().name
            selingrslst = select([self.ingredients_list]).where(
                self.ingredients_list.c.recipe_id == idx)
            ingredslstres = conn.execute(selingrslst)

            ings = []
            for ingredslstrow in ingredslstres:
                selingrds = select([self.ingredients]).where(
                    self.ingredients.c.id == ingredslstrow.ingredient_id)
                ingrdsresult = conn.execute(selingrds)
                for ingredsrow in ingrdsresult:
                    ing = Ingredient(
                        ingredsrow.name, ingredsrow.allergen, ingredslstrow.quantity)
                    ings.append(ing)

            seldirs = select([self.directions_list]).where(
                self.directions_list.c.recipe_id == idx)
            dirsresult = conn.execute(seldirs)
            dirs = []
            for dirsrow in dirsresult:
                dir = Direction(dirsrow.number, dirsrow.text)
                dirs.append(dir)

            recipex = Recipe(idx, recipesrow.name, recipesrow.country, recipesrow.course,
                            recipesrow.views, author, ings, recipesrow.image, dirs)

        return recipex

