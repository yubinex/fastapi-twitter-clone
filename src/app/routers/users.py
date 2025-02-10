from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.crud.users import create_user
from app.db_and_models.models import UserModel
from app.db_and_models.session import get_session

router = APIRouter(tags=["Users"])


@router.post("/users")
async def create_user_endpoint(
    user_model: UserModel, db: Session = Depends(get_session)
):
    return await create_user(user_model=user_model, db=db)
