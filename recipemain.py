from flask import Flask, render_template
from flask import request, session
from sqlalchemy.sql import select, func
from tabledef import *
from ingredient import *
from recipe import *
from direction import *
import os
import json

app = Flask(__name__)
engine = create_engine('sqlite:///recipes.db', echo=False)


# add a user with a password into the database
# if user exists already, return False
def user_register(uname, password, connection):
    s = select([users]).where(users.c.name == uname)
    result = connection.execute(s)
    rows = result.fetchall()
    amount = len(rows)
    if amount > 0:
        return False
    else:
        connection = engine.connect()
        ins = users.insert().values(name=uname, password=password)
        connection.execute(ins)
        return True


# authenticate a user against a password
# return False if failed
def user_authenticate(uname, password, connection):
    s = select([users]).where((users.c.name == uname)
                              & (users.c.password == password))
    result = connection.execute(s)
    rows = result.fetchall()
    amount = len(rows)
    if amount > 0:
        return True
    return False


# delete a user
def user_delete(uname, connection):
    res = users.delete(users.c.name == uname)
    connection.execute(res)


# return amount of users
def user_count(connection):
    res = select([users])
    result = connection.execute(res)
    rows = result.fetchall()
    return len(rows)


# return amount of recipes
def recipe_count(connection):
    res = select([recipes])
    result = connection.execute(res)
    rows = result.fetchall()
    return len(rows)


# return amount of ingredients
def ingredient_count(connection):
    res = select([ingredients])
    result = connection.execute(res)
    rows = result.fetchall()
    return len(rows)


# delete contents of database
def db_delete(connection):
    res = select([recipes])
    total = connection.execute(res)
    for x in total:
        recipe_delete(x.id, connection)

    res = select([users])
    total = connection.execute(res)
    for x in total:
        y = users.delete().where(users.c.id == x.id)
        connection.execute(y)


# delete all ingredients associated with a recipe (given an id of recipe)
def ingredients_delete(recipeid, connection):
    res = select([ingredients_list]).where(
        ingredients_list.c.recipe_id == recipeid)
    total = connection.execute(res)
    for x in total:
        res2 = ingredients.delete().where(ingredients.c.id == x.ingredient_id)
        connection.execute(res2)
    y = ingredients_list.delete().where(ingredients_list.c.recipe_id == recipeid)
    connection.execute(y)


# delete all directions associated with a recipe (given an id of recipe)
def directions_delete(recipeid, connection):
    res = select([directions_list])
    connection.execute(res)
    y = directions_list.delete().where(directions_list.c.recipe_id == recipeid)
    connection.execute(y)


# deletes a recipe and all it's data from the db
def recipe_delete(id, connection):
    ingredients_delete(id, connection)
    directions_delete(id, connection)
    res = recipes.delete().where(recipes.c.id == id)
    connection.execute(res)


# insert an ingredient into a recipe given the recipe id and an ingredient
def ingredient_insert(recipeid, ingredient, conn):

    s = select([recipes]).where(recipes.c.id == recipeid)
    result = conn.execute(s)
    one_row = result.fetchone()
    ins = ingredients.insert().values(
        name=ingredient['ingredient'], allergen=ingredient['allergen'])
    res = conn.execute(ins)
    ingredientpkey = res.inserted_primary_key
    ins = ingredients_list.insert().values(recipe_id=one_row.id,
                                           ingredient_id=ingredientpkey[0], quantity=ingredient['amount'])
    res = conn.execute(ins)


# insert a direction into a recipe given the recipe id and a direction and a number for the direction number
def direction_insert(recipeid, direction, num, conn):
    s = select([recipes]).where(recipes.c.id == recipeid)
    result = conn.execute(s)
    one_row = result.fetchone()
    ins = directions_list.insert().values(
        recipe_id=one_row.id, text=direction['direction'], number=num)
    conn.execute(ins)


# insert a recipe
def recipe_insert(name, author, country, course, ingreds, directions, image, connection):
    idx = 1
    s = select([users]).where(users.c.name == author)
    result = connection.execute(s)

    idx = result.fetchone().id
    if (image == ""):
        image = "default.png"

    ins = recipes.insert().values(name=name, country=country, course=course,
                                  image=image, views=int(0), user_id=idx)
    res = connection.execute(ins)
    recipepkey = res.inserted_primary_key
    num = int(0)

    for i in ingreds:
        ingredient_insert(recipepkey[0], i, connection)

    for i in directions:
        direction_insert(recipepkey[0], i, num, connection)
        num = num + 1

    return recipepkey[0]


# retrieve a recipe (as a Recipe object)
def recipe_get(idx, conn):
    selrecipes = select([recipes]).where(recipes.c.id == idx)
    recipesresult = conn.execute(selrecipes)

    recipex = ""

    for recipesrow in recipesresult:
        selusers = select([users]).where(users.c.id == recipesrow.user_id)
        usersresult = conn.execute(selusers)
        author = usersresult.fetchone().name
        selingrslst = select([ingredients_list]).where(
            ingredients_list.c.recipe_id == idx)
        ingredslstres = conn.execute(selingrslst)

        ings = []
        for ingredslstrow in ingredslstres:
            selingrds = select([ingredients]).where(
                ingredients.c.id == ingredslstrow.ingredient_id)
            ingrdsresult = conn.execute(selingrds)
            for ingredsrow in ingrdsresult:
                ing = Ingredient(
                    ingredsrow.name, ingredsrow.allergen, ingredslstrow.quantity)
                ings.append(ing)

        seldirs = select([directions_list]).where(
            directions_list.c.recipe_id == idx)
        dirsresult = conn.execute(seldirs)
        dirs = []
        for dirsrow in dirsresult:
            dir = Direction(dirsrow.number, dirsrow.text)
            dirs.append(dir)

        recipex = Recipe(idx, recipesrow.name, recipesrow.country, recipesrow.course,
                         recipesrow.views, author, ings, recipesrow.image, dirs)

    return recipex


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return list_recipes()


@app.route('/register', methods=['POST'])
def do_admin_register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    conn = engine.connect()
    success = user_register(POST_USERNAME, POST_PASSWORD, conn)
    conn.close()
    if not success:
        return('Name taken <br><a href=\'/\'>Try again</a>')
    else:
        return('Username created <br><a href=\'/\'>Login</a>')
    return home()


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    conn = engine.connect()
    success = user_authenticate(POST_USERNAME, POST_PASSWORD, conn)
    conn.close()
    if success:
        session['logged_in'] = True
        session['user'] = POST_USERNAME
    else:
        return 'Wrong password <a href=\'/\'>Try again</a>'
    return home()


@app.route('/searchexcludeallergen')
def searchexcludeallergen():
    allergen = request.args.get('allergen')
    conn = engine.connect()
    s = select([recipes])
    result = conn.execute(s)
    rs = []
    found = 0
    for row in result:
        select_st = select([ingredients_list]).where(
            ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([ingredients]).where(
                ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                if allergen.lower() == _row2.allergen.lower():
                    found = 1

        if found == 0:
            r = dict()
            r['id'] = row.id
            r['name'] = row.name
            r['country'] = row.country
            r['course'] = row.course
            r['image'] = row.image
            rs.append(r)
        else:
            found = 0

    conn.close()
    return json.dumps(rs)


@app.route('/searchbyingredient')
def searchbyingredient():
    ingredient = request.args.get('ingredient')
    s = select([recipes])
    conn = engine.connect()
    result = conn.execute(s)
    rs = []
    for row in result:
        select_st = select([ingredients_list]).where(
            ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([ingredients]).where(
                ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                if ingredient.lower() == _row2.name.lower():
                    r = dict()
                    r['id'] = row.id
                    r['name'] = row.name
                    r['country'] = row.country
                    r['course'] = row.course
                    r['image'] = row.image
                    rs.append(r)
    conn.close()
    return json.dumps(rs)


@app.route('/searchbycourse')
def searchbycourse():
    course = request.args.get('course')
    conn = engine.connect()
    s = select([recipes]).where(func.lower(
        recipes.c.course) == func.lower(course))

    rlist = []
    result = conn.execute(s)
    for row in result:
        r = dict()
        r['id'] = row.id
        r['name'] = row.name
        r['country'] = row.country
        r['course'] = row.course
        r['image'] = row.image
        rlist.append(r)
    conn.close()
    return json.dumps(rlist)


@app.route('/recipe')
def recipe():
    conn = engine.connect()
    idx = request.args.get('id')
    recipe = recipe_get(idx, conn)
    selrecipes = select([recipes]).where(recipes.c.id == idx)
    recipesresult = conn.execute(selrecipes)
    for recipesrow in recipesresult:
        stmt = recipes.update().values(
            views=(recipesrow.views + 1)).where(recipes.c.id == idx)
        conn.execute(stmt)

    conn.close()
    return render_template('recipe.html', recipe=recipe)


@app.route('/insertrecipe')
def insert_recipe():
    return render_template('insertrecipe.html', session=session)


@app.route('/ingredientstats')
def ingredientstats():
    conn = engine.connect()
    s = select([recipes])
    result = conn.execute(s)

    ings = []
    for row in result:
        select_st = select([ingredients_list]).where(
            ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([ingredients]).where(
                ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                found = 0
                for i in ings:

                    if i['ingredient'].lower() == _row2.allergen.lower():
                        i['amount'] = i['amount'] + 1
                        found = 1
                        break
                    else:
                        found = 0

                if found == 0 and _row2.allergen != '':
                    d = dict()
                    d['ingredient'] = _row2.allergen
                    d['amount'] = 1
                    ings.append(d)

    conn.close()
    return json.dumps(ings)


@app.route('/countrystats')
def countrystats():
    conn = engine.connect()
    s = select([recipes])
    result = conn.execute(s)
    crs = []

    for row in result:
        found = 0
        for i in crs:
            if i['country'].lower() == row.country.lower():
                i['amount'] = i['amount'] + 1
                found = 1
                break
            else:
                found = 0

        if found == 0:
            d = dict()
            d['country'] = row.country
            d['amount'] = 1
            crs.append(d)

    conn.close()
    return json.dumps(crs)


@app.route('/coursestats')
def coursestats():
    conn = engine.connect()
    s = select([recipes])
    result = conn.execute(s)
    crs = []

    for row in result:
        found = 0
        for i in crs:
            if i['course'].lower() == row.course.lower():
                i['amount'] = i['amount'] + 1
                found = 1
                break
            else:
                found = 0

        if found == 0:
            d = dict()
            d['course'] = row.course
            d['amount'] = 1
            crs.append(d)

    conn.close()
    return json.dumps(crs)


@app.route('/graphs')
def graphs():
    return render_template('graphs.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/listrecipes')
def list_recipes():
    s = select([recipes])
    conn = engine.connect()
    result = conn.execute(s)
    rs = []
    for row in result:
        recipe = recipe_get(row.id, conn)
        rs.append(recipe)

    conn.close()
    return render_template('listrecipes.html', recipes=rs)


@app.route('/updaterecipe', methods=['POST'])
def updaterecipe():
    content = request.get_json()
    conn = engine.connect()

    s = select([users]).where(users.c.name == content['author'])
    result = conn.execute(s)
    idx = result.fetchone().id

    ingredients_delete(content['id'], conn)
    directions_delete(content['id'], conn)

    num = int(0)
    for i in content['ingredients']:
        ingredient_insert(content['id'], i, conn)

    for i in content['directions']:
        direction_insert(content['id'], i, num, conn)
        num = num + 1

    s = select([recipes]).where(recipes.c.id == content['id'])
    result = conn.execute(s)
    x = result.fetchone()
    if x:
        idx = x.id
        stmt = recipes.update().values(course=content['course']).where(
            recipes.c.id == content['id'])
        conn.execute(stmt)
        stmt = recipes.update().values(country=content['country']).where(
            recipes.c.id == content['id'])
        conn.execute(stmt)
    conn.close()
    return 'Thank you'


@app.route('/insertrecipe', methods=['POST'])
def insertrecipe():
    conn = engine.connect()
    content = request.get_json()
    recipe_insert(content['name'], content['author'], content['country'], content['course'],
                  content['ingredients'], content['directions'], content['image'], conn)
    conn.close()
    return 'Thank you'


@app.route('/uploadajax', methods=['POST'])
def uploaded_file():
    file = request.files['file']
    if file:
        file.save(os.path.join("static", file.filename))

    return ''

@app.route('/deleterecipe', methods=['POST'])
def delete_recipe():
    content = request.get_json()
    conn = engine.connect()
    recipe_delete(content['id'], conn)
    conn.close()
    return ''


app.secret_key = os.urandom(12)
