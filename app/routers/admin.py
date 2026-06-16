from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/test")
async def admin_test():
    return {"message": "Admin router работает"}