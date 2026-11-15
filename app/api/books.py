from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import BookCreate, Book

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/", response_model=list[Book])
def list_books(category_id: int | None = None, db: Session = Depends(get_db)):
    if category_id is None:
        return crud.get_books(db)
    return crud.get_books_by_category(db, category_id)


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, data.title, data.description, data.price, data.category_id, data.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.put("/{book_id}", response_model= Book)
def update_book(book_id: int, data: BookCreate, db: Session = Depends(get_db)):
    if crud.get_book(db, book_id) is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    try:
        return crud.update_book(db, book_id, data.title, data.description, data.price, data.category_id, data.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if crud.get_book(db, book_id) is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    crud.delete_book(db, book_id)

