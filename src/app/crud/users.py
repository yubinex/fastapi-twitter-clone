from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.db_and_models.models import User, UserModel


async def create_user(user_model: UserModel, db: Session):
    existing_user = db.exec(select(User).where(User.email == user_model.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="email already in use")

    # TODO: hash password

    user = User.model_validate(user_model)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"success": f"user created with id {user.id}"}


async def login_user(form_data: OAuth2PasswordRequestForm, db: Session):
    existing_user = db.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="authentification failed")

    # TODO: validate password

    return {"access_token": "fake_token", "token_type": "bearer"}
