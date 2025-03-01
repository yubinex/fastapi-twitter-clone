from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.likes import create_like, delete_like, get_likes_of_post
from app.db_and_models.models import LikeModel, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Likes"])


@router.post("/likes")
async def create_like_endpoint(
    like_model: LikeModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_like(like_model=like_model, db=db, user_id=current_user.id)


@router.delete("/likes/{like_id}")
async def delete_like_endpoint(
    like_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_like(like_id=like_id, db=db, user_id=current_user.id)


@router.get("/posts/{post_id}/likes")
async def get_likes_of_post_endpoint(post_id: int, db: Session = Depends(get_session)):
    return await get_likes_of_post(post_id=post_id, db=db)
