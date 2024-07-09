from contextlib import asynccontextmanager
from typing import AsyncIterable

from fastapi import FastAPI

from src.app.infrastructure.database import init_db
from src.app.infrastructure.settings import settings
from src.app.routers import tokens_routers, users_routers


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_TITLE,
            version=settings.PROJECT_VERSION,
        )
        self._include_routers()

    def _include_routers(self) -> None:
        self.include_router(users_routers)
        self.include_router(tokens_routers)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterable:
    await init_db()
    yield


app = App(lifespan=lifespan)
