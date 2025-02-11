import datetime

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db_and_models.models import User

# TODO: move to environment variable
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_IN_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"])


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
