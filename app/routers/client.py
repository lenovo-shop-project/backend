from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import UserRole
from app.schemas.product import ProductResponse
from app.security import require_role
from app.services.product_service import ProductService
from app.schemas.category import CategoryResponse
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/client",
    tags=["Client"],
)


@router.get("/products", response_model=list[ProductResponse])
async def get_active_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_active_products()


@router.get("/categories", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_all_categories()


@router.get("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_role(UserRole.CLIENT))])
async def get_active_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_active_product_by_id(product_id)