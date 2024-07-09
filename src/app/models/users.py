from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    email: str = Field(default=None, nullable=False)
    username: str = Field(default=None, nullable=False)
    password: str = Field(default=None, nullable=False)
