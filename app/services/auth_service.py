from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def register(
        self,
        data: RegisterRequest,
    ) -> User:
        email = data.email.strip().lower()
        existing_user = await self.db.scalar(
            select(User).where(User.email == email)
        )
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует",
            )
        first_user_id = await self.db.scalar(
            select(User.id).limit(1)
        )
        if first_user_id is None:
            role = UserRole.ADMIN
        else:
            role = UserRole.CLIENT
        user = User(
            email=email,
            password_hash=hash_password(data.password),
            image_url=data.image_url,
            role=role,
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError as error:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует",
            ) from error
        return user


    async def login(
        self,
        data: LoginRequest,
    ) -> dict[str, str]:
        email = data.email.strip().lower()
        user = await self.db.scalar(
            select(User).where(User.email == email)
        )
        if user is None or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_access_token(user)
        return {
            "access_token": token,
            "token_type": "bearer",
        }