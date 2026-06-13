from fastapi import Header,HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from services.api_key_service import verify_api_key

def require_api_key(x_api_key:str = Header(...),db:Session = Depends(get_db)):
    if not verify_api_key(db,x_api_key):
        raise HTTPException(status_code=401,detail='Invalid or missing API key')
    return x_api_key