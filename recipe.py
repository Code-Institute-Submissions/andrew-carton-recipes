from flask import Flask, render_template
from flask import jsonify, request
from sqlalchemy.sql import table, column, select, update, insert
from tabledef import *
import os

app = Flask(__name__)
engine = create_engine('sqlite:///recipes.db', echo=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/insertrecipe')
def insert_recipe():
    return render_template('insertrecipe.html')

@app.route('/jsoninsertrecipe', methods = ['POST'])
def jsoninsertrecipe():
    content = request.get_json()
    conn = engine.connect() 
    ins = recipes.insert().values(name=content['name'], country=content['country'], views=int(0), user_id=1)
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

    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
