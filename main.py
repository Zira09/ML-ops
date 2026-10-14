from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import numpy as np
from scipy.sparse import csr_matrix
from typing import Optional

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the book app"}

class Book(BaseModel):
    id: int
    Title: str = Field(..., min_length = 1, max_length = 10)
    Author: str
    Price: float = Field(...)
    category: str
    year: int  

class BookRequest(BaseModel):
    Title: str = Field(..., min_length = 1, max_length = 10)
    Author: str
    Price: float = Field(...)
    category: str
    year: int 

class BookResponse(BaseModel):
    id: int
    Title: str = Field(..., min_length = 1, max_length = 10)
    Author: str
    Price: float = Field(...)
    category: str
    year: int 



class BookPatch(BaseModel):
    Title: Optional[str] = None
    Author: Optional[str] = None
    Price: Optional[float] = None
    category: Optional[str] = None
    year: Optional[int] = None

storage: list[Book] = []

@app.post("/addbooks/{id}", response_model=BookResponse, status_code=201)
def add_book( item: BookRequest, id: int = None):
    new_id = id if id is not None else len(storage) + 1
    stored = BookResponse(id=new_id, **item.model_dump())
    storage.append(stored)
    return stored

@app.get("/ourbooks")
def read_books():
    return storage   


@app.put("/updatedbooks/{id}")
def book_update1(item: BookRequest, id: int):
    for index, book in enumerate(storage):
        if book.id == id:
            updated_book = BookResponse(id=id, **item.model_dump())
            storage[index] = updated_book
    return updated_book

@app.patch("/updatedbooks/{id}")
def book_update2(item: BookPatch, id: int):
    for index, book in enumerate(storage):
        if book.id == id:
            updates = item.model_dump(exclude_unset=True)
            for field, value in updates.items():
                setattr(book, field, value)
    return book

@app.delete("/deletebook/{id}")
def book_delete(id: int):
    for book in storage:
        if book.id == id:
            storage.remove(book)
    return     

