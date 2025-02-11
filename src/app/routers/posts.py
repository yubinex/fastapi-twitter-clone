from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.posts import create_post, delete_post
from app.db_and_models.models import PostModel, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Posts"])


@router.post("/posts")
async def create_post_endpoint(
    post_model: PostModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_post(post_model=post_model, db=db, user_id=current_user.id)


@router.delete("/posts/{post_id}")
async def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_post(post_id=post_id, db=db, user_id=current_user.id)
