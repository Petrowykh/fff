from .init import (cursor, IntegrityError)
from model.creature import Creature
#from error import Missing, Duplicate

cursor.execute(""" create table if not exists creature(
                name text primary key,
                description text,
                country text,
                area text,
                aka text)               
            """)



def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name, description, country, area, aka)

def model_to_dict(creature: Creature) -> dict:
    return creature.dict()

def get_one(name: str) -> Creature:
    qry = "select * from creature where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    return row_to_model(cursor.fetchone())

def get_all() -> list[Creature]:
    qry = "select * from creature"
    cursor.execute(qry)
    rows = list(cursor.fetchall())
    return [row_to_model(row) for row in cursor.fetchall()]

def create(creature: Creature) -> Creature:
    qry = "insert into creature values (:name, :description, :country, :area, :aka)"
    params = model_to_dict(creature)
    cursor.execute(qry, params)
    return get_one(creature.name)

def modify(creature: Creature) -> Creature:
    qry = "update creature set country=:country, name=:name, description=:description, area=:area, aka=:aka where name=:name_orig"
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = cursor.execute(qry, params)
    return get_one(creature.name)

def delete(creature: Creature):
    qry = "delete from creature where name=:name"
    params = {"name": creature.name}
    res = cursor.execute(qry, params)
    return bool(res)

