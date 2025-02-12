from fastapi import FastAPI,HTTPException,Depends
from pydantic import  BaseModel
from uuid import UUID
from pydantic import Field
import  model
from database import SessionLocal,engine
from sqlalchemy.orm import Session
from sqlalchemy import select

app=FastAPI()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Book(BaseModel):
    #id:UUID we do not need it now because we have made it auto increment in our database
    title:str=Field(min_length=1)
    author:str=Field(min_length=1,max_length=100)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=-1,lt=101)

Books=[]

@app.get("/") #fetch/get books in the Books
def read_api(db:Session=Depends(get_db)):
    return db.query(model.Books).all()


@app.post("/") #create books
def create_books(book:Book,db:Session=Depends(get_db)):
    book_model=model.Books()
    book_model.title=book.title
    book_model.author=book.author
    book_model.description=book.description
    book_model.rating=book.rating
    db.add(book_model)
    db.commit()
    return Books

@app.put("/{book_id}")
def update_book(book_id:int ,book:Book,db:Session=Depends(get_db)):
    book_model=db.get(model.Books,book_id)
    # book_model = db.query(model.Books).filter(model.Books.id == book_id).first()

    if book_model is None:
        raise  HTTPException(
            status_code=404,
            detail=f"Book with id {book_id}: Does not Exist"
        )
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.get(model.Books, book_id)

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} does not exist"
        )

    db.delete(book_model)  # Correct deletion method
    db.commit()



# @app.post("/{book_id}")
# def update_books(book_id:UUID , book:Book):
#     counter=0
#     for x in Books:
#         counter +=1
#         if x.id==book_id:
#             Books[counter-1]=book
#             return Books[counter-1]
#     raise HTTPException(
#         status_code=404,
#         detail=f"ID{book_id}: Does not exist in the management system"
#     )

# def delete_books(book_id=UUID,book=Book):
#     counter=0
#     for x in Books:
#         counter+=1
#         if x.id==book_id:
#             del Books[counter-1]
#             return {f"Books with Book_id= {book_id}": "Deleted Successfully"}
#     raise  HTTPException(
#         status_code=404,
#         detail=f"Books with {book_id} does not exist in Books library"
#     )
#
