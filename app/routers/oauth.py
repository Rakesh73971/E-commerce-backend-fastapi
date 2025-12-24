from fastapi.security import OAuth2PasswordRequestForm
from .. import database,models,utils,oauth2
from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post('/')
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    access_token = oauth2.create_access_token(data={'user_id':user.id})

    return {'access_token':access_token,"token_type":"Bearer"}
    