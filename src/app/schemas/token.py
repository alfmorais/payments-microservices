from enum import Enum

from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None


class TokenType(Enum):
    BEARER = "bearer"


class BearerToken(BaseModel):
    access_token: str
    token_type: TokenType = TokenType.BEARER.value
