from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {
        "message": "user created",
        "data": user
    }

@app.get("/users")
def get_users():
    return users

@app.delete("/users")
def delete_users():
    users.clear()
    return {"message": "all users deleted"}