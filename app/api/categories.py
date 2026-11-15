from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import crud
from app.db.db import get_db
from app.schemas import Category, CategoryCreate

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.get("/", response_model=list[Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_category(db, data.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    if crud.get_category(db, category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    try:
        return crud.update_category(db, category_id, data.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    if crud.get_category(db, category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    crud.delete_category(db, category_id)
