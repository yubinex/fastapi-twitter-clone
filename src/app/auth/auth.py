import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.db_and_models.models import User
from app.db_and_models.session import get_session

# TODO: move to environment variable
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def create_access_token(user: User):
    try:
        claims = {
            "sub": user.username,
            "email": user.email,
            "exp": datetime.datetime.now()
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES),
        }
        return jwt.encode(claims=claims, key=SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise JWTError("token encoding failed")


def verify_token(token: str):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise JWTError("token decoding failed")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):
    payload = verify_token(token=token)
    username = payload.get("sub")
    user = db.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authorized")
    return user
