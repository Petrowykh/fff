from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
from service import explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix = "/explorer")

@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> Explorer:
    try:
        return service.get_one(name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)
    
@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except Duplicate as E:
        raise HTTPException(status_code=409, detail=E.msg)
    


@router.patch("/")
def modify(explorer: Explorer) -> Explorer:
    try:
        return service.modify(explorer)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)


@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as E:
        raise HTTPException(status_code=404, detail=E.msg)
    