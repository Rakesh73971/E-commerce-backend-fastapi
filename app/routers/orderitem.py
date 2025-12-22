from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import database,models,schemas
from typing import List


router = APIRouter(
    prefix='/orderitems',
    tags=['OrderItems']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.OrderItemResponse])
def get_orderitems(db:Session=Depends(database.get_db)):
    db_orderitems = db.query(models.OrderItem).all()
    return db_orderitems



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.OrderItemResponse)
def get_orderitem(id:int,db:Session=Depends(database.get_db)):
    db_orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == id).first()
    if db_orderitem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"orderitem with id {id} not found")
    return db_orderitem



@router.post('/',response_model=schemas.OrderItemResponse,status_code=status.HTTP_201_CREATED)
def create_orderitem(orderitem:schemas.OrderItemBase,db:Session=Depends(database.get_db)):
    db_orderitem = models.OrderItem(**orderitem.dict())
    db.add(db_orderitem)
    db.commit()
    db.refresh(db_orderitem)
    return db_orderitem

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_orderitem(id:int,db:Session=Depends(database.get_db)):
    db_orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == id).first()
    if db_orderitem is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"orderitem with id {id} not found")
    db.delete(db_orderitem)
    db.commit()
    return {'message':'orderitem was deleted'}

@router.put('/{id}',status_code=status.HTTP_201_CREATED,response_model=schemas.OrderItemResponse)
def update_orderitem(id:int,orderitem:schemas.OrderItemUpdate,db:Session=Depends(database.get_db)):
    db_orderitem = db.query(models.OrderItem).filter(models.OrderItem.id == id)
    existing_db = db_orderitem.first()
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"order item with id {id} not found")
    db_orderitem.update(orderitem.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_orderitem = db_orderitem.first()
    return updated_orderitem