from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException

app = FastAPI(title="Book Tracker API ", version ="1.0.0")

books_db=[]

@app.get("/")
def read_root():
    return {"message":"Welcome to book tracker API!","status":"running"}

class Book(BaseModel):
    title:str
    author:str
    status:str = 'want_to_read'
    rating:Optional[int] = None

current_id =1

@app.get("/books")

def get_all_books():
    return books_db

@app.post("/books")

def add_book(book:Book):
    global cuurent_id
    new_book = Book(id=current_id,**book.dict())
    books_db.append(book)
    return {"message":"book added successfully","book":book}

@app.get("/books/{book_id}")
def get_book(book_id:int):
    for book in books_db:
        if book.id == book_id:
            return book
    return{"error":"book not found"}    
    