import os
import asyncio
from fastapi import Header,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client,Client
from sqlalchemy.orm import Session
from database import get_db
from services.api_key_service import verify_api_key

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

supabase:Client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
)

def require_api_key(x_api_key:str = Header(...),db:Session = Depends(get_db)):
    if not verify_api_key(db,x_api_key):
        raise HTTPException(status_code=401,detail='Invalid or missing API key')
    return x_api_key

async def get_current_user_id(token :str = Depends(oauth2_scheme)) -> str:

    try:
        user_data = await asyncio.to_thread(supabase.auth.get_user, token)

        if not user_data or not user_data.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={"WWW-Authenticate": "Bearer"}
            )
        return str(user_data.user.id)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={"WWW-Authenticate": "Bearer"}
        )

