from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# -------------------- FASTAPI APP --------------------

app = FastAPI()


# -------------------- DATABASE CONFIG --------------------

DATABASE_URL = "postgresql://book_user:book123@localhost/book_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# -------------------- SQLALCHEMY MODEL (DB TABLE) --------------------

class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    language = Column(String)


# Create table if not exists
Base.metadata.create_all(bind=engine)


# -------------------- PYDANTIC MODELS --------------------

class Book(BaseModel):      # Request & Response model
    id: int
    title: str
    author: str
    language: str

    class Config:
        from_attributes = True


class BookUpdateModel(BaseModel):      # For PATCH
    title: str
    author: str
    language: str


# -------------------- DB DEPENDENCY --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- ROUTES --------------------

@app.get("/books", response_model=List[Book])
async def get_all_books(db: Session = Depends(get_db)):
    return db.query(BookDB).all()


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book, db: Session = Depends(get_db)) -> dict:
    new_book = BookDB(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/book/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)) -> dict:
    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book


@app.patch("/book/{book_id}")
async def update_book(
    book_id: int,
    book_update_date: BookUpdateModel,
    db: Session = Depends(get_db)
) -> dict:

    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found thus not updated"
        )

    book.title = book_update_date.title
    book.author = book_update_date.author
    book.language = book_update_date.language

    db.commit()
    db.refresh(book)
    return book


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found thus not deleted"
        )

    db.delete(book)
    db.commit()
    return {}
