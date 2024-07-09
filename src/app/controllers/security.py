import os
from datetime import datetime, timedelta
from typing import Dict

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from zoneinfo import ZoneInfo

from src.app.infrastructure.database import get_session
from src.app.infrastructure.exceptions import Credentials
from src.app.models.users import User
from src.app.schemas.token import TokenData

TOKEN_SECRET = os.environ["TOKEN_SECRET"]
TOKEN_ALGORITHM = os.environ["TOKEN_ALGORITHM"]
TOKEN_EXPIRE_TIME = int(os.environ["TOKEN_EXPIRE_TIME"])
OAUTH2 = OAuth2PasswordBearer(tokenUrl="/v1/token")


class PasswordController:
    def __init__(self) -> None:
        self.pwd_context = PasswordHash.recommended()

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


class TokenJwtController:
    def __init__(self, secret: str, algorithm: str, expire_time: int) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.expire_time = expire_time

    def create_access_token(self, data: Dict) -> Dict:
        to_encode = data.copy()
        now = datetime.now(tz=ZoneInfo("UTC"))
        expire = now + timedelta(minutes=self.expire_time)
        to_encode.update({"exp": expire})
        encoded_jwt = encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt


async def current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(OAUTH2),
) -> User:
    try:
        payload = decode(token, TOKEN_SECRET, algorithms=[TOKEN_ALGORITHM])
        username: str = payload["sub"]

        if not username:
            Credentials.raise_exception()

        token_data = TokenData(username=username)

    except (DecodeError, KeyError):
        Credentials.raise_exception()

    statement = select(User).where(User.email == token_data.username)
    result = await session.exec(statement)
    user = result.one_or_none()

    if not user:
        Credentials.raise_exception()

    return user


password_controller = PasswordController()
token_controller = TokenJwtController(
    secret=TOKEN_SECRET,
    algorithm=TOKEN_ALGORITHM,
    expire_time=TOKEN_EXPIRE_TIME,
)
