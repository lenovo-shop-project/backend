from fastapi import APIRouter, Depends
from app.models.user import UserRole
from app.security import require_role


router = APIRouter(
    prefix="/client",
    tags=["Client"],
    dependencies=[
        Depends(require_role(UserRole.CLIENT)),
    ],
)


@router.get("/test")
def client_test():
    return {
        "message": "Доступ клиента разрешён",
    }