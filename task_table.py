from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # とりあえず全部許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#SQLite版
# import sqlite3

# conn = sqlite3.connect("tasks.db", check_same_thread=False)
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS tasks (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT
# )
# """)
# conn.commit()

#SQLAlchemy版（DB接続）
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#モデル作成（テーブル定義）
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

#テーブル作成
Base.metadata.create_all(bind=engine)

#tasks = []　メモリ用

class Task(BaseModel):
    title: str


@app.post("/tasks")
def create_task(task: Task):
    db = SessionLocal()

    new_task = TaskModel(title=task.title)
    db.add(new_task)
    db.commit()

    return {"message": "Task added"}

@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(TaskModel).all()

    return [{"id": t.id, "title": t.title} for t in tasks]

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    db = SessionLocal()

    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        task.title = updated_task.title
        db.commit()

    return {"message": "Updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()

    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()

    return {"message": "Deleted"}

# @app.post("/tasks")　単体で渡すバージョン
# def create_task(task: Task):
#     tasks.append(task)
#     return {"message": "Task added"}


# @app.post("/tasks/bulk")　Listで渡すバージョン
# def create_tasks(tasks_input: List[Task]):
#     for task in tasks_input:
#         tasks.append(task)
#     return {"message": "Tasks added"}

#task_id = 1　メモリ用↓

# @app.post("/tasks")　エンドポイントを単体とListで分けないバージョン
# def create_task(tasks_input: Union[Task, List[Task]]):
#     global task_id
#     if isinstance(tasks_input, list):
#         for task in tasks_input:
#             tasks.append({
                
#               "id": task_id,
#                 "title": task.title

#             })
#             task_id += 1
#         return {"message": "Tasks added"}
#     else:
#         tasks.append({ "id": task_id,
#             "title": tasks_input.title
#             })
#         task_id += 1
#         return {"message": "Task added"}

# @app.get("/tasks")
# def get_tasks():
#     return tasks

# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, updated_task: Task):
#     for task in tasks:
#         if task["id"] == task_id:
#             task["title"] = updated_task.title
#             return {"message": "Updated"}
#     return {"error": "Not found"}

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):
#     global tasks
#     tasks = [task for task in tasks if task["id"] != task_id]
#     return {"message": "Deleted"}
#     return {"error": "Not found"}

