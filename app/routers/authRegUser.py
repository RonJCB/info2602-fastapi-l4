from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import  AuthDep
#from fastapi.security import OAuth2PasswordRequestForm
#from typing import Annotated
from fastapi import status

regUser_router = APIRouter(tags = ["RegularUser"])

#Exercise1 updating response datamodel for todos route so it returns a list of 
#category items whereby a single cat item should show the Id of the category and the
#category text
@regUser_router.get("/todos",response_model=list[TodoResponse])
def get_Todos(db: SessionDep, user:AuthDep):
    todos = db.exec(select(RegularUser).where(RegularUser.todos.user_id == user.id)).all()

    if not todos:
        raise HTTPException(
         status_code=status.HTTP_404_UNAUTHORIZED,
            detail="Todos not found in Database",
            headers={"WWW-Authenticate": "Bearer"},
        )#error validation
    return todos

@regUser_router.get("/todo{id}", response_model = UserResponse)
def get_todo_byid(id:int ,db: SessionDep , user:AuthDep):
    todo = db.exec(select(Todo).where(Todo.id == id , Todo.user_id == user.id)).one_or_none()

    if not todo:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Todo not found in Database by that ID",
            headers={"WWW-Authenticate": "Bearer"},
        )  
    return todo

@regUser_router.post("/todos", response_model=TodoResponse) 
async def create_todo(db:SessionDep, user:AuthDep, todo: TodoCreate):
    todo = Todo(text=todo.text, user_id=user.id)
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while creating an item",)

@regUser_router.put("/todo{id}", response_model = TodoResponse)
async def update_todo(db:SessionDep, user:AuthDep, todoState: TodoUpdate):
    todo = db.exec(select(Todo).where(Todo.id == user.todos.id)).one_or_none()

    if not todo:
        raise HTTPException(
              status_code = status.HTTP_405_METHOD_NOT_ALLOWED,
         detail = "Cannot updateTodo in database",
         headers = {"WindowsError"} , 
        )
    if (todoState.text):
        todo.text = todoState.text
    elif(todoState.done):
        todo.done = todoState.done
    try:
        db.add(todo)
        db.commit()
        return todo
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while updating an item",
        )
@regUser_router.delete("/todo/{id}")
async def delete_todo(id:int ,db:SessionDep , user:AuthDep):
    todo = db.exec(select(Todo).where(Todo.user_id == user.id, Todo.id == id)).one_or_none()
    if not todo:
        raise HTTPException(
         status_code = status.HTTP_405_METHOD_NOT_ALLOWED,
         detail = "Cannot delete Todo in database",
         headers = {"WindowsError"} , 
        )
    try:

        db.delete(todo)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while deleting an item",
        )
