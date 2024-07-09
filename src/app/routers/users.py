from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.controllers import password_controller
from src.app.infrastructure.database import get_session
from src.app.models import User
from src.app.schemas import UserPayload, UserResponse

router = APIRouter(tags=["Users"], prefix="/v1/users")


@router.post(
    "",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    description="Endpoint para criar um usuário da API",
)
async def create_user(
    user: UserPayload,
    session: AsyncSession = Depends(get_session),
):
    hashed_password = password_controller.get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
    )

    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    return new_user
