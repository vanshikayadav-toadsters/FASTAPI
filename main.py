# from fastapi import FastAPI

# from typing import Optional

# app = FastAPI()

# user_list = [
#    "Jerry",
#    "Joey",
#    "Phil"
# 

# @app.get('/search')
# async def search_for_user(username: str):
#     if username in user_list:
#         return {"message": f"details for user {username}"}
#     else:
#         return {"message": "User Not Found"}



# from typing import Optional

# @app.get('/greet/')
# async def greet(username:Optional[str]="User"):
#    return {"message":f"Hello {username}"}




# A simple pydantic model

# from pydantic import BaseModel

# users=[]

# # the User model
# class UserSchema(BaseModel):
#    username:str
#    email:str


# @app.post("/create_user")
# async def create_user(user_data:UserSchema):
#    new_user = {
#       "username" : user_data.username,
#       "email": user_data.email
#    }

#    users.append(new_user)

#    return {"message":"User Created successfully","user":new_user}






#connecting routers_tutorial.py to main.py
# main.py
# from fastapi import FastAPI
# from routers_tutorials import router

# app = FastAPI()

# app.include_router(router)




from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Books
from pydantic import BaseModel

app=FastAPI()

Base.metadata.create_all(bind=engine)

class BookCreate(BaseModel):
    title:str
    author:str


def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()



@app.post("/books")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book=Books(title=book.title , author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books")
def get_books(db: Session=Depends(get_db)):
    return db.query(Books).all()

    


