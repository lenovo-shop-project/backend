from fastapi import APIRouter, Depends
from app.models.user import UserRole
from app.security import require_role


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[
        Depends(require_role(UserRole.ADMIN)),
    ],
)


@router.get("/test")
def admin_test():
    return {
        "message": "Доступ администратора разрешён",
    }