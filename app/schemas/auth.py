from pydantic import BaseModel, ConfigDict, Field
from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=255,
    )

    password: str = Field(
        min_length=6,
        max_length=128,
    )

    image_url: str | None = Field(
        default=None,
        max_length=500,
    )


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: UserRole
    image_url: str | None