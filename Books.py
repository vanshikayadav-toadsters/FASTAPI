from fastapi import FastAPI , status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

app= FastAPI()


books=[
    {
    
        "id":1,
        "title":"Think Python",
        "author":"Allen",
        "language":"English"
    },

    {
        "id":2,
        "title":"FastApi",
        "author":"Rock",
        "language":"English"
        
    }
    
]

class Book(BaseModel):      #PYDANTIC MODEL 
                            #DEFINES Field Name and Field Type
    id:int
    title:str
    author:str
    language:str


class BookUpdateModel(BaseModel):      #For PATCH requests
                                       #Necessary for validation
                                       #Only the field names mentioned can be updated
    title:str
    author:str
    language:str
                    

@app.get("/books",response_model=List[Book])         #RESPONSE MODEL is just used for response. It returns shape and body which we have to return to the client
async def get_all_books():                 
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict :
    new_book=book_data.model_dump()       #Model dump converts pydantic model into python dictionary 
    books.append(new_book)
    return new_book



@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")


@app.patch("/book/{book_id}")
async def update_book(book_id:int,book_update_date:BookUpdateModel) -> dict:            #Book_id is given for which we have to update the data
    global books
    for book in books:
        if book["id"] == book_id:
            book['title'] = book_update_date.title
            book['author'] = book_update_date.author
            book['language'] = book_update_date.language

            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found thus not updated")
    

@app.delete("/book/{book.id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
        for book in books:
            if book["id"] == book_id:
                books.remove(book)

                return {}
    
            
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found thus not deleted")






