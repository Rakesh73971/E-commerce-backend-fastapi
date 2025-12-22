from fastapi import APIRouter,status,HTTPException,Depends
from .. import database,models,schemas
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.ProductResponse])
def get_products(db:Session=Depends(database.get_db)):
    products = db.query(models.Product).all()
    return products



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ProductResponse)
def get_prodct(id:int,db:Session=Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'product with id {id} not found')
    return product


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.ProductResponse)
def create_product(product:schemas.Product,db:Session=Depends(database.get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session=Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'product with id {id} not found')
    db.delete(db_product)
    db.commit()
    return {'message':'successfully deleted the product'}

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.ProductResponse)
def update_product(id:int,product:schemas.ProductUpdate,db:Session=Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id)
    existing_product = db_product.first()
    if existing_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'product with id {id} not found')
    db_product.update(product.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_product = db_product.first()
    return updated_product