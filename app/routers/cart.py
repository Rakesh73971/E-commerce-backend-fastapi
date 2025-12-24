from fastapi import HTTPException,status,Depends,APIRouter
from .. import models,schemas,database
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/carts',
    tags=['Cart']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.CartResponse])
def cart_items(db:Session=Depends(database.get_db)):
    carts = db.query(models.Cart).all()
    return carts


@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.CartResponse)
def cart_item(id:int,db:Session=Depends(database.get_db)):
    db_cart = db.query(models.Cart).filter(models.Cart.id == id).first()
    if db_cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cart with id {id} not found')
    return db_cart



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.CartResponse)
def create_cart(cart:schemas.CartBase,db:Session=Depends(database.get_db)):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id:int,db:Session=Depends(database.get_db)):
    db_query = db.query(models.Cart).filter(models.Cart.id == id).first()
    if db_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cart with id {id} not found')
    db.delete(db_query)
    db.commit()
    return {'message':'successfully deleted the cart'}

