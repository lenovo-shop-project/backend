from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.get("/test")
async def auth_test():
    return {"message": "Auth router работает"}