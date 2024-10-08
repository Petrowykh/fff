from .init import (cursor, IntegrityError)
from model.explorer import Explorer
from error import Missing, Duplicate

cursor.execute("""create table if not exists explorer(
                name text primary key,
                country text, 
                description text)""")


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.dict() if explorer else None


def get_one(name: str) -> Explorer:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    cursor.execute(qry, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Explorer with name {name} not found")


def get_all() -> list[Explorer]:
    qry = "select * from explorer"
    cursor.execute(qry)
    return [row_to_model(row) for row in cursor.fetchall()]


def create(explorer: Explorer) -> Explorer:
    qry = "insert into explorer (name, country, description) values (:name, :country, :description)"
    params = model_to_dict(explorer)
    try:
        cursor.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Explorer with name {explorer.name} already exists")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    qry = "update explorer set country=:country, name=:name, description=:description where name=:name_orig"
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    cursor.execute(qry, params)
    if cursor.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(f"Explorer with name {explorer.name} not found")
    


def delete(explorer: Explorer) -> bool:
    qry = "delete from explorer where name = :name"
    params = {"name": explorer.name}
    cursor.execute(qry, params)
    if cursor.rowcount != 1:
        raise Missing(f"Explorer with name {explorer.name} not found")
    
