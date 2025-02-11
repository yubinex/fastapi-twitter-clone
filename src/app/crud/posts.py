from fastapi import HTTPException
from sqlmodel import Session, select

from app.db_and_models.models import Post, PostModel, User


async def create_post(post_model: PostModel, db: Session, user_id: int):
    existing_user = db.exec(select(User).where(User.id == user_id)).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="user not found")

    post = Post(
        content=post_model.content, created_at=post_model.created_at, user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"success": "post created", "post_id": post.id, "user_id": user_id}


async def delete_post(post_id: int, db: Session, user_id: int):
    post = db.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.user_id != user_id:
        raise HTTPException(
            status_code=401,
            detail="unauthorized: you can only delete posts that you created.",
        )

    db.delete(post)
    db.commit()
    return {"success": f"post with id {post_id} deleted"}
