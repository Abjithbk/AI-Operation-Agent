import os
import asyncio
from fastapi import Request,HTTPException,Depends,status
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

def require_api_key(request:Request,db:Session = Depends(get_db)):
    api_key = request.headers.get('X-API-KEY')

    if not api_key:
        raise HTTPException(status_code=401,detail='API key required')
    user_id = verify_api_key(db,api_key)
    if not user_id:
        raise HTTPException(status_code=401,detail="Invalid API key")
    
    return user_id

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

