from flask import Flask, render_template
from flask import request, session
from sqlalchemy.sql import select, func, desc
from recipedatabase import RecipeDatabase
import os
from os import listdir
from os.path import isfile, join
import json


app = Flask(__name__)
database = RecipeDatabase("recipes.db")

@app.route('/')
def home():
    mypath = 'static/images/'
    allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files = []
    for f in allfiles:
        if f == "recipe-background.jpg" or f == 'default.png':
            continue
        else:
            files.append(f)

    return render_template('login.html', files=files)
    


@app.route('/register', methods=['POST'])
def do_admin_register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    conn = database.engine.connect()
    success = database.user_register(POST_USERNAME, POST_PASSWORD, conn)
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
    conn = database.engine.connect()
    success = database.user_authenticate(POST_USERNAME, POST_PASSWORD, conn)
    conn.close()
    if success:
        session['logged_in'] = True
        session['user'] = POST_USERNAME
    else:
        return 'Wrong password <a href=\'/\'>Try again</a>'
    return list_recipes()


@app.route('/searchexcludeallergen')
def searchexcludeallergen():
    allergen = request.args.get('allergen')
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)
    rs = []
    found = 0
    for row in result:
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([database.ingredients]).where(
                database.ingredients.c.id == _row.ingredient_id)
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
    s = select([database.recipes])
    conn = database.engine.connect()
    result = conn.execute(s)
    rs = []
    for row in result:
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([database.ingredients]).where(
                database.ingredients.c.id == _row.ingredient_id)
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
    conn = database.engine.connect()
    s = select([database.recipes]).where(func.lower(
        database.recipes.c.course) == func.lower(course))

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
    conn = database.engine.connect()
    idx = request.args.get('id')
    recipe = database.recipe_get(idx, conn)
    selrecipes = select([database.recipes]).where(database.recipes.c.id == idx)
    recipesresult = conn.execute(selrecipes)
    for recipesrow in recipesresult:
        stmt = database.recipes.update().values(
            views=(recipesrow.views + 1)).where(database.recipes.c.id == idx)
        conn.execute(stmt)

    conn.close()
    return render_template('recipe.html', recipe=recipe)


@app.route('/insertrecipe')
def insert_recipe():
    if session.get('logged_in'):
        return render_template('insertrecipe.html', session=session)
    else:
        return home()


@app.route('/ingredientstats')
def ingredientstats():
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)

    ings = []
    for row in result:
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        for _row in res:
            select_st2 = select([database.ingredients]).where(
                database.ingredients.c.id == _row.ingredient_id)
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
    conn = database.engine.connect()
    s = select([database.recipes])
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
    conn = database.engine.connect()
    s = select([database.recipes])
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
    s = select([database.recipes]).order_by(desc(database.recipes.c.id))
    conn = database.engine.connect()
    result = conn.execute(s)
    rs = []
    for row in result:
        recipe = database.recipe_get(row.id, conn)
        rs.append(recipe)

    conn.close()
    return render_template('listrecipes.html', recipes=rs)


@app.route('/updaterecipe', methods=['POST'])
def updaterecipe():
    content = request.get_json()
    conn = database.engine.connect()

    s = select([database.users]).where(database.users.c.name == content['author'])
    result = conn.execute(s)
    idx = result.fetchone().id

    database.ingredients_delete(content['id'], conn)
    database.directions_delete(content['id'], conn)

    num = int(0)
    for i in content['ingredients']:
        database.ingredient_insert(content['id'], i, conn)

    for i in content['directions']:
        database.direction_insert(content['id'], i, num, conn)
        num = num + 1

    s = select([database.recipes]).where(database.recipes.c.id == content['id'])
    result = conn.execute(s)
    x = result.fetchone()
    if x:
        idx = x.id
        stmt = database.recipes.update().values(course=content['course']).where(
            database.recipes.c.id == content['id'])
        conn.execute(stmt)
        stmt = database.recipes.update().values(country=content['country']).where(
            database.recipes.c.id == content['id'])
        conn.execute(stmt)
    conn.close()
    return 'Thank you'


@app.route('/insertrecipe', methods=['POST'])
def insertrecipe():
    conn = database.engine.connect()
    content = request.get_json()
    database.recipe_insert(content['name'], content['author'], content['country'], content['course'],
                  content['ingredients'], content['directions'], content['image'], conn)
    conn.close()
    return 'Thank you'


@app.route('/uploadajax', methods=['POST'])
def uploaded_file():
    file = request.files['file']
    if file:
        file.save(os.path.join("static/images/", file.filename))

    return ''

@app.route('/deleterecipe', methods=['POST'])
def delete_recipe():
    content = request.get_json()
    conn = database.engine.connect()
    database.recipe_delete(content['id'], conn)
    conn.close()
    return ''


app.secret_key = os.urandom(12)
