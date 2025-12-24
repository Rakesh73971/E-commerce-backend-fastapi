from fastapi import FastAPI,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,database
from .. import utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {id} not found')
    return user


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.User,db:Session=Depends(database.get_db)):
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user