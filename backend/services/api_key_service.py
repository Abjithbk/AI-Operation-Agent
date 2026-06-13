import secrets
from sqlalchemy.orm import Session
from models import ApiKey

def generate_api_key(db:Session,name:str):
    new_key = 'aiops_'+secrets.token_urlsafe(32)

    api_key = ApiKey(
        key = new_key,
        name=name,
        is_active = 'true'
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key

def verify_api_key(db:Session,key:str) -> bool:
    api_key = db.query(ApiKey).filter(
        ApiKey.key == key,
        ApiKey.is_active == 'true'
    ).first()

    return api_key is not None