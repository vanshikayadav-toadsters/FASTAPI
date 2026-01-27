from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter(prefix="/books",tags=["Hello"])

class Book(BaseModel):
    title:str
    author:str

@router.get("/")
def get_books():
    return {"message" : "All books "}

@router.get("/{books.id}")
def get_book(book_id:int):
    return {"book_id": book_id}

@router.post("/")
def create_book(book:Book):
    return{
        "message":"Book added",
        "book":book
    }