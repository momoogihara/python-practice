from fastapi import APIRouter
router = APIRouter()

@router.get("/add")
def add(a :int,b:int):
    return{"result" :a+b}