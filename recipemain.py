from flask import Flask, render_template
from flask import request, session
from sqlalchemy.sql import select, func, desc
from recipedatabase import RecipeDatabase
import os
from os import listdir
from os.path import isfile, join
import json


app = Flask(__name__)

# Specify the database to use for the application
database = RecipeDatabase("recipes.db")

"""
    The function home() and root route '/'
    Render template 'login.html' with static files and the session

"""


@app.route('/')
def home():

    # Get all the images in the static directory for the carousel
    mypath = 'static/images/'
    allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files = []

    # Exclude the background and default images from the carousel
    for f in allfiles:
        if f == "recipe-background.jpg" or f == 'default.png':
            continue
        else:
            files.append(f)

    # Pass the files into the template for rendering the carousel
    return render_template('login.html', files=files, session=session)


"""
    The function do_register() and app route '/register'
    Do server side checking of the username and password
    for registration purposes, and provide errors if username
    is already taken or password is inadequate
"""


@app.route('/register', methods=['POST'])
def do_register():
    # Deserialise JSON to content data
    content = request.get_json()

    # Check if username is sufficient -- if not provide error message
    if len(content['username']) <= 3 or len(content['username']) > 20:
        return json.dumps({'success': False, 'message':
                           'Username must be greater than 3 characters'
                           ' and smaller than 20'})

    # Check if password is sufficient -- if not provide error message
    if len(content['password']) <= 3 or len(content['password']) > 20:
        return json.dumps({'success': False, 'message':
                           'Password must be greater than 3 characters'})

    # If safety checks are passed, connect to database
    conn = database.engine.connect()
    # Register user
    success = database.user_register(
        content['username'], content['password'], conn)
    conn.close()
    # If return is success return a success message otherwise provide
    #  username taken error message in json
    if success:
        return json.dumps({'success': True})
    else:
        return json.dumps({'success': False, 'message': 'Username taken'})


"""
    The function do_login and app route '/login':
    Do server side checking of username and password for login purposes,
    and provide errors if username
    or password is adequate or authentication has failed

"""


@app.route('/login', methods=['POST'])
def do_login():
    # Deserialise JSON from frontend
    content = request.get_json()

    # Do some checking of username string length and provide
    # error message if inadequate
    if len(content['username']) <= 3 or len(content['username']) > 20:
        return json.dumps({'success': False, 'message': 'Username must be'
                           ' greater than 3 characters and smaller than 20'})

    # Same for password
    if len(content['password']) <= 3 or len(content['password']) > 20:
        return json.dumps({'success': False, 'message':
                           'Password must be greater than 3 characters'})

    # Connect to database and attempt to authenicate
    conn = database.engine.connect()
    success = database.user_authenticate(
        content['username'], content['password'], conn)
    conn.close()

    # If authentication successful set session variables and print success
    # Otherwise provide error in JSON back to frontend
    if success:
        session['logged_in'] = True
        session['user'] = content['username']
        return json.dumps({'success': True})
    else:
        return json.dumps({'success': False, 'message':
                           'Authentication failed'})




"""
    Function: search -- '/search'.
    This is an AJAX function to provide the frontend with recipes
    tailored to the search criteria
"""


def append_duplicates(rs):
    new_rs = []
    seen = set()
        
    for d in rs:
        # Change to tuple to hash
        t = tuple(d.items())
        if t not in seen:
            # Add to set
            seen.add(t)
        else:
            new_rs.append(d)

    return new_rs

@app.route('/search')
def search():
    # Get the attributes from URL
    allergen = request.args.get('allergen')
    course = request.args.get('course')
    ingredient = request.args.get('ingredient')

    # Recipes list
    rs = []
    """ Algorithm:
        if all three searches:
            - get intersection of the three
        else if any two
            - get intersection of the two
        else if any one
            -return list
    """

    if allergen and course and ingredient:
        rs.extend(searchexcludeallergen(allergen))
        rs.extend(searchbycourse(course))
        rs = append_duplicates(rs)
        rs.extend(searchbyingredient(ingredient))
        rs = append_duplicates(rs)
    elif (allergen and course):
        rs.extend(searchexcludeallergen(allergen))
        rs.extend(searchbycourse(course))
        rs = append_duplicates(rs)
    elif (allergen and ingredient):
        rs.extend(searchexcludeallergen(allergen))
        rs.extend(searchbyingredient(ingredient))
        rs = append_duplicates(rs)
    elif (course and ingredient):
        rs.extend(searchbycourse(course))
        rs.extend(searchbyingredient(ingredient))
        rs = append_duplicates(rs)
    elif allergen:
        rs.extend(searchexcludeallergen(allergen))
    elif course:
        rs.extend(searchbycourse(course))
    elif ingredient:
        rs.extend(searchbyingredient(ingredient))
    
    return json.dumps(rs)


"""
    Function: searchexcludeallergen
    This is an AJAX function to provide the frontend with recipes
    tailored to an 'exclude allergen' search
"""


def searchexcludeallergen(allergen):
    if not allergen or allergen == '':
        return []
    # Connect to Database and get recipes
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)

    # Recipes list
    rs = []

    # Set if allergen found
    found = 0

    # Iterate over recipes 'row' in 'results'
    for row in result:
        # Get the ingredient list of that recipe
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        # For each ingredient in the ingredient list
        # Get the allergen
        for _row in res:
            select_st2 = select([database.ingredients]).where(
                database.ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                if allergen.lower() == _row2.allergen.lower():
                    found = 1

        # If the allergen is not found in the recipe -- append it to list
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
    return rs


"""
    Function: searchbyingredient 
    This is an AJAX function to provide the frontend with recipes
    tailored to an 'ingredient' search
"""


def searchbyingredient(ingredient):
    if not ingredient or ingredient == '':
        return []
    # Get all recipes
    s = select([database.recipes])
    conn = database.engine.connect()
    result = conn.execute(s)
    # List of recipes
    rs = []

    # For each recipe 'row' in the recipes list
    # Get the ingredients list of that recipe
    for row in result:
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        # For each ingredient in the ingredients list check to see
        # if the ingredient 'ingredient' is found.
        # If it is, add to 'rs' list
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
    return rs


"""
    Function searchbycourse 
    Search for recipes in database by course e.g. starter, main.
    This is an AJAX function that provides data to the frontend
"""


def searchbycourse(course):

    if not course or course == '':
        return []
    # Connect to database and select by course (case insenstivie match)
    conn = database.engine.connect()
    s = select([database.recipes]).where(func.lower(
        database.recipes.c.course) == func.lower(course))

    # List to hold data
    rlist = []
    result = conn.execute(s)

    # Add each recipe 'row' from 'result' into the list
    for row in result:
        r = dict()
        r['id'] = row.id
        r['name'] = row.name
        r['country'] = row.country
        r['course'] = row.course
        r['image'] = row.image
        rlist.append(r)
    conn.close()

    return rlist


"""
    Function recipe() - app route '/recipe'
    Retrieves the ID of the recipe from the URL
    and then retrieves that recipe from database, and passes
    it to recipe.html template.

    Also updates the 'views' counter of that recipe

"""


@app.route('/recipe')
def recipe():
    conn = database.engine.connect()
    # Get ID from URL
    idx = request.args.get('id')
    # Get the recipe from the database
    recipe = database.recipe_get(idx, conn)
    selrecipes = select([database.recipes]).where(database.recipes.c.id == idx)
    recipesresult = conn.execute(selrecipes)

    # Update the views counter in that recipe
    for recipesrow in recipesresult:
        stmt = database.recipes.update().values(
            views=(recipesrow.views + 1)).where(database.recipes.c.id == idx)
        conn.execute(stmt)

    # Close connection
    conn.close()
    # Pass recipe to template
    return render_template('recipe.html', recipe=recipe)


"""
    Function insert_recipe : app route '/insertrecipe'

    Renders insertrecipe.html template if user is logged in

"""


@app.route('/insertrecipe')
def insert_recipe():
    if session.get('logged_in'):
        return render_template('insertrecipe.html', session=session)
    else:
        return home()


"""
    Function ingredientstats() - app route '/ingredientstats'

    This is an AJAX function for the frontend that provides statistics on the
    amount of allergens in ingredients
"""


@app.route('/ingredientstats')
def ingredientstats():
    # Connect to database and get all recipes
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)

    # Ingredient dictionary list 'ingredient name' as key 'amount' as value
    ings = []
    # Get Ingredient List of each recipe
    for row in result:
        select_st = select([database.ingredients_list]).where(
            database.ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)

        # Iterate over ingredients in ingredient list
        for _row in res:
            select_st2 = select([database.ingredients]).where(
                database.ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                # Set if allergen is found
                found = 0
                # Iterate over each allergen found already in
                # the ingredients list
                for i in ings:
                    # If found increase the amount of the allergen by one
                    if i['ingredient'].lower() == _row2.allergen.lower():
                        i['amount'] = i['amount'] + 1
                        found = 1
                        break
                    else:
                        # Reset found variable
                        found = 0

                # If not found in the ingredient allergen list
                # Add a new dictionary entry for that allergen
                if found == 0 and _row2.allergen != '':
                    d = dict()
                    d['ingredient'] = _row2.allergen
                    d['amount'] = 1
                    ings.append(d)

    conn.close()
    # Dictionary to JSON serialisation
    return json.dumps(ings)


"""
    Function countrystats - app route '/countrystats'
    This is an AJAX function for the frontend to provide stats
    for the countries in the recipe database for the graphs
"""


@app.route('/countrystats')
def countrystats():
    # Connect to database and get all recipes
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)
    # Dictionary List - country as key, amount as value
    crs = []

    # Get the country in each recipe
    for row in result:
        found = 0
        for i in crs:
            # Case insenstivee match
            if i['country'].lower() == row.country.lower():
                i['amount'] = i['amount'] + 1
                found = 1
                break
            else:
                found = 0

        # If not found add the entry to dictionary
        if found == 0:
            d = dict()
            d['country'] = row.country
            d['amount'] = 1
            crs.append(d)

    conn.close()
    # Serialise the dictionary list to JSON
    return json.dumps(crs)


"""
    Function coursetats - app route '/coursestats'
    This is an AJAX function for the frontend to provide stats
    for the courses in the recipe database for the graphs
"""


@app.route('/coursestats')
def coursestats():
    # Connect to database and get recipes
    conn = database.engine.connect()
    s = select([database.recipes])
    result = conn.execute(s)

    # Courses dictionary list - course key / amount value
    crs = []

    for row in result:
        found = 0
        for i in crs:
            # Case insensitive match
            if i['course'].lower() == row.course.lower():
                # If found increment
                i['amount'] = i['amount'] + 1
                found = 1
                break
            else:
                found = 0

        # Add course if not already in list
        if found == 0:
            d = dict()
            d['course'] = row.course
            d['amount'] = 1
            crs.append(d)

    conn.close()
    # Serialise dictionary list to JSON
    return json.dumps(crs)


"""
    Function graphs() - app route '/graphs'
    Render the graphs.html template
"""


@app.route('/graphs')
def graphs():
    return render_template('graphs.html')


"""
    Function logout() - app route '/logout'
    Set the session logged_in to False
"""


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


"""
    Function list_recipes - app route '/listrecipes'.
    Get recipes ordered by last in first out
    and pass to template listrecipes.html
"""


@app.route('/listrecipes')
def list_recipes():
    # Order by last first
    s = select([database.recipes]).order_by(desc(database.recipes.c.id))
    conn = database.engine.connect()
    result = conn.execute(s)
    rs = []
    for row in result:
        # Get recipe
        recipe = database.recipe_get(row.id, conn)
        rs.append(recipe)

    conn.close()
    return render_template('listrecipes.html', recipes=rs)


"""
    Function updaterecipe() - app route '/updateroute'
    Updates the recipe with JSON from frontend
"""


@app.route('/updaterecipe', methods=['POST'])
def updaterecipe():
    # Deserialise JSON to content dictionary
    content = request.get_json()
    conn = database.engine.connect()

    # Get the User ID of the author
    s = select([database.users]).where(
        database.users.c.name == content['author'])
    result = conn.execute(s)

    # Delete all ingredients and directions of the 'id' of the recipe
    database.ingredients_delete(content['id'], conn)
    database.directions_delete(content['id'], conn)

    # Insert new ingredients and directions into database
    num = int(0)
    for i in content['ingredients']:
        database.ingredient_insert(content['id'], i, conn)

    for i in content['directions']:
        database.direction_insert(content['id'], i, num, conn)
        num = num + 1

    # Get the recipe
    s = select([database.recipes]).where(
        database.recipes.c.id == content['id'])
    result = conn.execute(s)
    x = result.fetchone()
    if x:
        # Update the course and country data
        stmt = database.recipes.update().values(course=content['course']).where(
            database.recipes.c.id == content['id'])
        conn.execute(stmt)
        stmt = database.recipes.update().values(country=content['country']).where(
            database.recipes.c.id == content['id'])
        conn.execute(stmt)
    conn.close()
    return 'Thank you'


"""
    Function insertrecipe - app route '/insertrecipe'
    Insert recipe into database
"""


@app.route('/insertrecipe', methods=['POST'])
def insertrecipe():
    conn = database.engine.connect()
    # Deserialise json from frontend to content dictionary
    content = request.get_json()
    # Insert with new data
    database.recipe_insert(content['name'], content['author'],
                           content['country'], content['course'],
                           content['ingredients'], content['directions'],
                           content['image'], conn)
    conn.close()
    return 'Thank you'


"""
    Function uploaded_file - app route '/uploadajax'
    Upload a file to the static/images directory
"""


@app.route('/uploadajax', methods=['POST'])
def uploaded_file():
    file = request.files['file']
    if file:
        # Save to this directory
        file.save(os.path.join("static/images/", file.filename))

    return ''


"""
    Function delete_recipe - app route '/deleterecipe'
    Delete a recipe with 'id' given
"""


@app.route('/deleterecipe', methods=['POST'])
def delete_recipe():
    content = request.get_json()
    conn = database.engine.connect()
    # Delete from database
    database.recipe_delete(content['id'], conn)
    conn.close()
    return ''


app.secret_key = os.urandom(12)
