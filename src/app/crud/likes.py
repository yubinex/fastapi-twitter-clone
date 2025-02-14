from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Like, LikeModel, Post, User


async def create_like(like_model: LikeModel, db: Session, user_id: int):
    # check if user exists with id
    existing_user = db.exec(select(User).where(User.id == user_id)).first()
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail=f"could not find user with id: {user_id}",
        )
    # check if post exists with id
    existing_post = db.exec(select(Post).where(Post.id == like_model.post_id)).first()
    if not existing_post:
        raise HTTPException(
            status_code=404,
            detail=f"could not fund post with id: {like_model.post_id}",
        )
    # check if post is already liked
    existing_like = db.exec(
        select(Like)
        .where(Like.user_id == user_id)
        .where(Like.post_id == like_model.post_id)
    ).first()
    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="user has already liked this post",
        )
    like = Like(post_id=like_model.post_id, user_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return {"success": "like added"}


async def delete_like(like_id: int, db: Session, user_id: int):
    existing_like = db.exec(select(Like).where(Like.id == like_id)).first()
    if not existing_like:
        raise HTTPException(
            status_code=404,
            detail="like not found",
        )
    if existing_like.user_id == user_id:
        raise HTTPException(
            status_code=401,
            detail="users can only remove their own likes",
        )
    db.delete(existing_like)
    db.commit()
    return {"success": "like removed"}
