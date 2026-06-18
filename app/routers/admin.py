from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import UserRole
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.security import require_role
from app.services.product_service import ProductService
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[
        Depends(require_role(UserRole.ADMIN)),
    ],
)


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.create_product(data)


@router.patch("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.update_product(
        product_id=product_id,
        data=data,
    )


@router.patch("/products/{product_id}/deactivate", response_model=ProductResponse)
async def deactivate_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.deactivate_product(product_id)


@router.patch("/products/{product_id}/activate", response_model=ProductResponse)
async def activate_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.activate_product(product_id)


@router.get("/products", response_model=list[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_all_products_admin()


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_product_by_id_admin(product_id)

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.create_category(data)