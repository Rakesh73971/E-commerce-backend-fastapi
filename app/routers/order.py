from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import database,models,schemas
from ..oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix='/orders',
    tags=['Order']
)


@router.get('/',response_model=List[schemas.OrderResponse],status_code=status.HTTP_200_OK)
def get_orders(db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    orders = db.query(models.Order).all()
    return orders



@router.post('/',response_model=schemas.OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(order:schemas.OrderBase,db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    order = models.Order(**order.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order



@router.get('/{id}',response_model=schemas.OrderResponse,status_code=status.HTTP_200_OK)
def get_order(id:int,db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"order with id {id} not found")
    return db_order



@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id:int,db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    db_order = db.query(models.Order).filter(models.Order.filter == id).first()
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"order with id {id} not found")
    db.delete(db_order)
    db.commit()
    return {"message":"successfully deleted the order"}


@router.put('/{id}',response_model=schemas.OrderResponse)
def update_order(id:int,order:schemas.OrderUpdate,db:Session=Depends(database.get_db),current_user=Depends(get_current_user)):
    db_order = db.query(models.Order).filter(models.Order.id == id)
    db_existing = db_order.first()
    if db_existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'order with id {id} not found')
    db_order.update(order.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_order = db_order.first()
    return updated_order