from http import HTTPStatus

from fastapi import HTTPException


class Credentials:
    @staticmethod
    def raise_exception() -> HTTPException:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class IncorrectEmailOrPassword:
    @staticmethod
    def raise_exception() -> HTTPException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )
