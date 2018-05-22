from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.sql import select
from tabledef import *
 
engine = create_engine('sqlite:///recipes.db', echo=True)

conn = engine.connect() 
#ins = users.insert().values(name='andrew', password='test')
#conn.execute(ins)

#del_st = recipes.delete().where(
#      recipes.c.name == 'Stew')
#res = conn.execute(del_st)

   
s = select([recipes])
result = conn.execute(s)
for row in result:
    print(row.id)

    select_st = select([ingredients_list]).where(ingredients_list.c.recipe_id == row.id)
    res = conn.execute(select_st)
    for _row in res: print _row

    select_st = select([directions_list]).where(ingredients_list.c.recipe_id == row.id)
    res = conn.execute(select_st)
    for _row in res: print _row


