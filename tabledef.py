
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine

engine = create_engine('sqlite:///recipes.db', echo=True)

metadata = MetaData()

users = Table('users', metadata,
     Column('id', Integer, primary_key=True),
     Column('name', String),
     Column('password', String)
)

recipes = Table('recipes', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('country', String, nullable=False),
        Column('views', Integer, nullable=False),
        Column('user_id', None, ForeignKey('users.id'))
)

ingredients = Table('ingredients', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('allergen', String),
)

ingredients_list = Table('ingredients_list', metadata,
        Column('recipe_id', None, ForeignKey('recipes.id')),
        Column('ingredient_id', None, ForeignKey('ingredients.id')),
        Column('quantity', String, nullable=False)
)

directions_list = Table('directions_list', metadata, 
        Column('recipe_id', None, ForeignKey('recipes.id')),
        Column('text', String, nullable=False),
        Column('number', Integer, nullable=False)
)

metadata.create_all(engine)