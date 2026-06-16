from fastapi import APIRouter

router = APIRouter(
    prefix="/client",
    tags=["Client"],
)


@router.get("/test")
async def client_test():
    return {"message": "Client router работает"}