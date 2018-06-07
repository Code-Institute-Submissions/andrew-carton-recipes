from flask import Flask, render_template
from flask import jsonify, request, session
from sqlalchemy.sql import table, column, select, update, insert
from tabledef import *
from ingredient import *
from recipe import *
from direction import *
import os

app = Flask(__name__)
engine = create_engine('sqlite:///recipes.db', echo=True)

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
    s = select([users]).where(users.c.name == POST_USERNAME)
    result = conn.execute(s)
    rows = result.fetchall()
    lenro = len(rows)
    if lenro > 0:
        return('Name taken <br><a href=\'/\'>Try again</a>')
    else:
        conn = engine.connect() 
        ins = users.insert().values(name=POST_USERNAME, password=POST_PASSWORD)
        res = conn.execute(ins)
        return('Username created <br><a href=\'/\'>Login</a>')
    return home()
    
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    conn = engine.connect() 
    s = select([users]).where((users.c.name == POST_USERNAME) & (users.c.password == POST_PASSWORD))
    result = conn.execute(s)
    rows = result.fetchall()
    lenro = len(rows)
    if lenro > 0 :
        session['logged_in'] = True
        session['user'] = POST_USERNAME
    else:
        return ('Wrong password <a href=\'/\'>Try again</a>')
    return home()


 
@app.route('/recipe')
def recipe():
    id = request.args.get('id')
    conn = engine.connect() 
    s = select([recipes]).where(recipes.c.id == id)
    result = conn.execute(s)
    recipe = ""
    for row in result:
        select_st = select([ingredients_list]).where(ingredients_list.c.recipe_id == id)
        res = conn.execute(select_st)
            
        ings = []
        for _row in res:
            select_st2 = select([ingredients]).where(ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                ing = Ingredient(_row2.name, _row2.allergen, _row.quantity)
                ings.append(ing)
    
        
        select_st = select([directions_list]).where(directions_list.c.recipe_id == id)
        res = conn.execute(select_st)
        dirs = []
        for _row in res:
            dir = Direction(_row.number, _row.text)
            dirs.append(dir)
        
        recipe = Recipe(id, row.name, row.country, row.course, row.views, ings, dirs)
    
    return render_template('recipe.html', recipe=recipe)
    
@app.route('/insertrecipe')
def insert_recipe():
    return render_template('insertrecipe.html', session=session)

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
        select_st = select([ingredients_list]).where(ingredients_list.c.recipe_id == row.id)
        res = conn.execute(select_st)
        
        ings = []
        for _row in res:
            select_st2 = select([ingredients]).where(ingredients.c.id == _row.ingredient_id)
            res2 = conn.execute(select_st2)
            for _row2 in res2:
                print _row2
                ing = Ingredient(_row2.name, _row2.allergen, _row.quantity)
                ings.append(ing)

    
        select_st = select([directions_list]).where(directions_list.c.recipe_id == row.id)
        res = conn.execute(select_st)
        dirs = []
        for _row in res:
            dir = Direction(_row.number, _row.text)
            dirs.append(dir)
    
        recipe = Recipe(row.id, row.name, row.country, row.course, row.views, ings, dirs)
        rs.append(recipe)
    
    return render_template('listrecipes.html', recipes=rs)
    

@app.route('/jsoninsertrecipe', methods = ['POST'])
def jsoninsertrecipe():
    content = request.get_json()
    conn = engine.connect() 
    ins = recipes.insert().values(name=content['name'], country=content['country'], course=content['course'], views=int(0), user_id=1)
    res = conn.execute(ins)
    recipepkey = res.inserted_primary_key
    
    
    num = int(0);
    for i in content['ingredients']:
        ins = ingredients.insert().values(name=i['ingredient'], allergen=i['allergen'])
        res = conn.execute(ins)
        ingredientpkey = res.inserted_primary_key
        ins = ingredients_list.insert().values(recipe_id=recipepkey[0], ingredient_id=ingredientpkey[0], quantity=i['amount'])
        res = conn.execute(ins)
    
    
    for i in content['directions']:
        ins = directions_list.insert().values(recipe_id=recipepkey[0], text=i['direction'], number=num)
        res = conn.execute(ins)
        num = num + 1
        
    
    return 'Thank you'

app.secret_key = os.urandom(12)
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
