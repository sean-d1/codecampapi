from jose import JWTError, jwt
import datetime
from datetime import datetime, timedelta, UTC
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        decoded_token = jwt.decode(
            token, key=settings.secret_key, algorithms=settings.algorithm
        )
        id = decoded_token.get("user_id")
    except JWTError:
        raise credentials_exception

    if id is None:
        raise credentials_exception

    token_data = schemas.TokenData(id=id)
    return token_data


def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.get(models.User, token.id)

    return user.id
