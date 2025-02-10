from fastapi import HTTPException
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
