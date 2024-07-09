from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.app.controllers import (
    current_user,
    password_controller,
    token_controller,
)
from src.app.infrastructure.database import get_session
from src.app.infrastructure.exceptions import IncorrectEmailOrPassword
from src.app.models import User
from src.app.schemas import BearerToken, TokenType

router = APIRouter(tags=["Token"], prefix="/v1")


@router.post(
    "/token",
    response_model=BearerToken,
    status_code=HTTPStatus.CREATED,
    description="Endpoint para criar um Token JWT",
)
async def create_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    statement = select(User).filter(User.email == credentials.username)
    result = await session.exec(statement)
    user = result.one_or_none()

    if not user:
        IncorrectEmailOrPassword.raise_exception()

    is_valid_password = password_controller.verify_password(
        credentials.password,
        user.password,
    )
    if not is_valid_password:
        IncorrectEmailOrPassword.raise_exception()

    access_token = token_controller.create_access_token(
        data={"sub": user.email},
    )
    token = {
        "access_token": access_token,
        "token_type": TokenType.BEARER.value,
    }
    return token


@router.post(
    "/refresh-token",
    response_model=BearerToken,
    status_code=HTTPStatus.OK,
    description="Endpoint para atualizar um Token JWT",
)
async def create_refresh_token(user: User = Depends(current_user)):
    new_access_token = token_controller.create_access_token(
        data={"sub": user.email},
    )
    token = {
        "access_token": new_access_token,
        "token_type": TokenType.BEARER.value,
    }
    return token
