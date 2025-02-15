from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.auth.auth import get_current_user
from app.crud.followers import create_follower, delete_follower
from app.db_and_models.models import FollowerModel, User
from app.db_and_models.session import get_session

router = APIRouter(tags=["Followers"])


@router.post("/followers")
async def create_follower_endpoint(
    follower_model: FollowerModel,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_follower(
        follower_model=follower_model, db=db, user_id=current_user.id
    )


@router.delete("/followers/{follower_id}")
async def delete_follower_endpoint(
    follower_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await delete_follower(
        follower_id=follower_id, db=db, user_id=current_user.id
    )
