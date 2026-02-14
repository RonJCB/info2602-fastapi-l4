from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import AuthDep
#from fastapi.security import OAuth2PasswordRequestForm
#from typing import Annotated
from fastapi import status

catUser_router = APIRouter(tags = ["CategoryManagement"])
#Exercise2
#Creates a category for the CURRENT LOGGED IN user
@catUser_router.post("/category", response_model= CategoryResponse)
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
            detail = "Not authorized to create category listing",
        )

#add a category reponse model to see changes on client
#Assigns the category cat_id to the todo todo_id if the user is authorized to access it
@catUser_router.post("/todo/{todo_id}/category/{cat_id}", response_model = TodoCategory)
#must utilize the TodoCategory which maps the relationship to a user todo and a user Category
async def add_category(todoCat: TodoCategory, db:SessionDep, user:AuthDep, category_id:int, todo_id:int):
         todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
         if not todo:#if find dthaat todo with category id assignment
              raise HTTPException(
                   status_code = status.HTTP_404_NOT_FOUND,
                   detail = "Todo with that category Id not  found in database",
           #based on the category and the level of urgency for example
           # you can assign a todo to that todoCategory
           #Category table should mainly be used to classify the type of complexity
           #and or urgency of each todo class
           # for example category id 203 and 202 have urgent class so
           # their todo category will be mapped to the same todo category        
              )
         cat = db.exec(select(Category).where(Category.id == category_id)).one_or_none()
         if not cat:
               raise HTTPException(
                     status_code = status.HTTP_404_NOT_FOUND,
                     detail = "Category not found in database",
               )
    
        
         #create that todocategory listing if not there
         new_Category = TodoCategory(
            category_id = category_id
            ,todo_id = todo_id

        )
         todoCat.category_id = cat.id
         todoCat.todo_id = todo.id
         #todo.category.append(new_Category) 
         db.add(new_Category)
         db.commit()#add to db
         db.refresh(new_Category)
         return new_Category

@catUser_router.delete("/todo/{todo_id}/category/{cat_id}")
def delete_Category(db:SessionDep, user:AuthDep, cat_id:int, todo_id:int):
             todo = db.exec(select(Todo).where(Todo.id ==todo_id)).one_or_none()
             if not todo:
                raise HTTPException(
                        status_code= status.HTTP_404_NOT_FOUND,
                        detail ="Todo with that category assignment not found in db",
                )
             category = db.exec(select(Category).where(Category.id == cat_id)).one_or_none()
             if not category:
                   raise HTTPException(
                         status_code= status.HTTP_404_NOT_FOUND,
                        detail ="Todo with that category assignment not found in db",   
                   )
             todoCat = db.exec(select(TodoCategory).where(TodoCategory.todo_id == todo.id)).one_or_none()
             try:
                 db.delete(todoCat)
                 db.commit()
             except Exception:
                  db.rollback()
                  raise HTTPException(
                        status_code = status.HTTP_403_FORBIDDEN,
                        detail = "Error occurredd while trying to delete user"
                  )
@catUser_router.get("/category/{cat_id}/todos", response_model = list[TodoResponse])
async def get_Todos(db:SessionDep, user:AuthDep, cat_id:int):
            getTodoByCategory = db.exec(select(Category).where(Category.id == cat_id)).one_or_none()
            if not getTodoByCategory:
                  raise HTTPException(
                        status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Todos Categories by that ID not found in db",
                  )
            getTodoCat = db.exec(select(TodoCategory).where(TodoCategory.category_id == getTodoByCategory.id)).all()
            getAllTodos = db.exec(select(Todo).where(Todo.id == getTodoCat.todo_id)).all()
            if not getAllTodos:
                raise HTTPException(
                        status_code= status.HTTP_404_NOT_FOUND,
                        detail ="Todos not found in db",
                )
           
            return getAllTodos