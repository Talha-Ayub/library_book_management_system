from fastapi import FastAPI,HTTPException
from pydantic import  BaseModel
from uuid import UUID
from pydantic import Field

app=FastAPI()

class Book(BaseModel):
    id:UUID
    title:str=Field(min_length=1)
    author:str=Field(min_length=1,max_length=100)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=101)

Books=[]

@app.get("/") #fetch/get books in the Books
def check_books():
    return Books


@app.post("/") #create books
def add_books(book:Book):
    Books.append(book)
    return Books

@app.post("/{book_id}")
def update_books(book_id:UUID , book:Book):
    counter=0
    for x in Books:
        counter +=1
        if x.id==book_id:
            Books[counter-1]=book
            return Books[counter-1]
    raise HTTPException(
        status_code=404,
        detail=f"ID{book_id}: Does not exist"
    )

def delete_books(book_id=UUID,book=Book):
    counter=0
    for x in Books:
        counter+=1
        if x.id==book_id:
            del Books[counter-1]
            return {f"Books with Book_id= {book_id}": "Deleted Successfully"}
    raise  HTTPException(
        status_code=404,
        detail=f"Books with {book_id} does not exist in Books library"
    )

