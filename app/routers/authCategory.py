from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import encrypt_password, verify_password, create_access_token, AuthDep
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import status

catUser_router = APIRouter("tags = [CategoryManagement]")
#Exercise2
#Creates a category for the CURRENT LOGGED IN user
@catUser_router.post("/category", response_model= Category)
async def create_category(db:SessionDep, user:AuthDep, cat: Category):
    new_Category = Category(text = cat.text, 
                                id = cat.id , user_id =user.id )

    try:
        db.add(new_Category)
        db.commit()
        db.refresh(new_Category)
        return new_Category
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            details = "Not authorized to create category listing",
        )

#add a category reponse model to see changes on client
#Assigns the category cat_id to the todo todo_id if the user is authorized to access it
@catUser_router.post("/todo/{todo_id}/category/{cat_id}", response_model = TodoCategory)
async def add_category(db:SessionDep, user:AuthDep, category:Category):
         todo = db.exec(select(Todo).where(Todo.user_id == user.id )).one_or_none()
         if todo:#if find dthaat todo with category id assignment
              raise HTTPException(
                   status_code = status.HTTP_404_UNAUTHORIZED,
                   details = "Todo with that category Id already found in database"
                   
              )
         cat = db.exec(select(Category).where(Category.id == category.id)).one_or_none()
         if cat:
               raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     details = "Category already found in database",
               )
    
        
         #create that todocategory listing if not there
         new_Category = TodoCategory(
            category_id = category.id
            ,todo_id = todo.id
        )
         
         db.add(new_Category)
         db.commit()#add to db
         db.refresh(new_Category)
         return new_Category

@catUser_router.delete("/todo/{todo_id}/category/{cat_id}")
def delete_Category(db:SessionDep, user:AuthDep, cat:Category):
             todo = db.exec(select(Todo).where(Todo.user_id == user.id)).one_or_none()
             if not todo:
                raise HTTPException(
                        status_code= status.HTTP_404_NOT_FOUND,
                        details ="Todo with that category assignment not found in db",
                )
             category = db.exec(select(Category).where(Category.id == cat.id)).one_or_none()
             if not category:
                   raise HTTPException(
                         status_code= status.HTTP_404_NOT_FOUND,
                        details ="Todo with that category assignment not found in db",   
                   )
             todoCat = db.exec(select(TodoCategory).where(TodoCategory.todo_id == todo.id
                                                          , TodoCategory.category_id == category.id))
             db.delete(todoCat)
             db.commit()

@catUser_router.get("/category/{cat_id}/todos")
async def get_Todos(db:SessionDep, user:AuthDep, cat:Category):
            getTodoByCategory = db.exec(select(Category).where(Category.user_id == user.id, Category.id == cat.id)).all()
            if not getTodoByCategory:
                  raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        details = "Todos Categories by that ID not found in db",
                  )
            getTodos = db.exec(select(Todo).where(Todo.user_id == user.id, getTodoByCategory.id == cat.id)).all()

            if not getTodos:
                raise HTTPException(
                        status_code= status.HTTP_404_NOT_FOUND,
                        details ="Todos not found in db",
                )
           
            return getTodos