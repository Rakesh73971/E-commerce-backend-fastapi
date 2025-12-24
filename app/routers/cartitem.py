from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,database,schemas
from typing import List

router = APIRouter(
    prefix='/cartitems',
    tags=['CartItems']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.CartItemResponse])
def get_cartitems(db:Session=Depends(database.get_db)):
    cartitems = db.query(models.CartItem).all()
    return cartitems

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.CartItemResponse)
def get_cartitem(id:int,db:Session=Depends(database.get_db)):
    cartitem = db.query(models.CartItem).filter(models.CartItem.id == id).first()
    if cartitem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cartitem with id {id} not found')
    return cartitem


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.CartItemResponse)
def create_cartitem(cartitem:schemas.CartItemBase,db:Session=Depends(database.get_db)):
    db_query = models.CartItem(**cartitem.dict())
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_cartitems(id:int,db:Session=Depends(database.get_db)):
    db_query = db.query(models.CartItem).filter(models.CartItem.id == id).first()
    if db_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cart item with id {id} not found')
    db.delete(db_query)
    db.commit()
    return {'message':'successfully deleted the cart item'}


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.CartItemResponse)
def cart_item_update(id:int,cartitem:schemas.CartItemUpdate,db:Session=Depends(database.get_db)):
    db_query = db.query(models.CartItem).filter(models.CartItem.id == id)
    existing_db = db_query.first()
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cart item with id {id} not found')
    db_query.update(cartitem.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_cartitems = db_query.first()
    return updated_cartitems
