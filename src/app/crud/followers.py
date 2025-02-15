from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Follower, FollowerModel, User


async def create_follower(follower_model: FollowerModel, db: Session, user_id: int):
    current_user = db.exec(select(User).where(User.id == user_id)).first()
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="current user not found",
        )
    followed_user = db.exec(
        select(User).where(User.id == follower_model.follower_id)
    ).first()
    if not followed_user:
        raise HTTPException(
            status_code=404,
            detail="user to follow not found",
        )

    already_followed = db.exec(
        select(Follower)
        .where(Follower.user_id == user_id)
        .where(Follower.follower_id == follower_model.follower_id)
    ).first()
    if already_followed:
        raise HTTPException(
            status_code=400,
            detail=f"current user is already following user with id {follower_model.follower_id}",
        )

    follower = Follower(follower_id=follower_model.follower_id, user_id=user_id)
    db.add(follower)
    db.commit()
    db.refresh(follower)
    return {"success": f"user with id: {user_id} now follows {follower.follower_id}"}
