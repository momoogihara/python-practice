from fastapi import APIRouter
router = APIRouter()

@router.get("/users/{name}/age/{age}")
def get_user(name: str, age:int):
    return{"name" : name , "age" : age}