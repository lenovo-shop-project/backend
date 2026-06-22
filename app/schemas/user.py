from pydantic import BaseModel, ConfigDict


class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    image_url: str | None