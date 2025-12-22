from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import database,models,schemas
from typing import List

router = APIRouter(
    prefix='/categories',
    tags=['Categories']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.CategoryResponse])
def get_categories(db:Session=Depends(database.get_db)):
    categories = db.query(models.Category).all()
    return categories


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.CategoryResponse)
def get_category(id:int,db:Session=Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'category with id { id } not found')
    return category


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.CategoryResponse)
def create_category(category:schemas.Category,db:Session=Depends(database.get_db)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id:int,db:Session=Depends(database.get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'category with id {id} not found')
    db.delete(db_category)
    db.commit()
    return {"message":"successfully deleted the category"}
