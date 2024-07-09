from pydantic import BaseModel, EmailStr


class UserPayload(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
