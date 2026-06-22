from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _is_valid_transition(
        self,
        current_status: OrderStatus,
        new_status: OrderStatus,
    ) -> bool:
        valid_transitions = {
            OrderStatus.CREATED: {
                OrderStatus.PAID,
                OrderStatus.CANCELLED,
            },
            OrderStatus.PAID: {
                OrderStatus.SHIPPED,
                OrderStatus.CANCELLED,
            },
            OrderStatus.SHIPPED: {
                OrderStatus.COMPLETED,
            },
            OrderStatus.COMPLETED: set(),
            OrderStatus.CANCELLED: set(),
        }
        return new_status in valid_transitions[current_status]

    async def _get_order_or_404(
        self,
        order_id: int,
    ) -> Order:
        order = await self.db.scalar(
            select(Order)
            .options(
                selectinload(Order.items),
            )
            .where(
                Order.id == order_id,
            )
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заказ не найден",
            )
        return order

    async def _get_active_product_or_404(
        self,
        product_id: int,
    ) -> Product:
        product = await self.db.scalar(
            select(Product).where(
                Product.id == product_id,
                Product.is_available == true(),
            )
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден",
            )
        return product

    async def _restore_stock(
        self,
        order: Order,
    ) -> None:
        for item in order.items:
            product = await self.db.get(
                Product,
                item.product_id,
            )

            if product is not None:
                product.stock += item.quantity

    async def create_order(
        self,
        data: OrderCreate,
        current_user: User,
    ) -> Order:
        product_ids = [
            item.product_id for item in data.items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Один товар нельзя добавлять в заказ несколько раз",
            )

        order = Order(
            user_id=current_user.id,
            status=OrderStatus.CREATED,
            total_amount=Decimal("0.00"),
        )

        self.db.add(order)

        await self.db.flush()

        total_amount = Decimal("0.00")

        for item_data in data.items:
            product = await self._get_active_product_or_404(
                item_data.product_id,
            )

            if product.stock < item_data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Недостаточно товара на складе: {product.name}",
                )

            product.stock -= item_data.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=product.price,
            )

            self.db.add(order_item)

            total_amount += product.price * item_data.quantity

        order.total_amount = total_amount
        await self.db.commit()
        return await self._get_order_or_404(
            order.id,
        )

    async def get_my_orders(
        self,
        current_user: User,
    ) -> list[Order]:
        result = await self.db.scalars(
            select(Order)
            .options(
                selectinload(Order.items),
            )
            .where(
                Order.user_id == current_user.id,
            )
            .order_by(
                Order.created_at.desc(),
            )
        )
        return list(result.all())

    async def cancel_my_order(
        self,
        order_id: int,
        current_user: User,
    ) -> Order:
        order = await self._get_order_or_404(
            order_id,
        )

        if order.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Нет доступа к этому заказу",
            )

        if order.status in {
            OrderStatus.SHIPPED,
            OrderStatus.COMPLETED,
        }:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Нельзя отменить отправленный или завершённый заказ",
            )

        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Заказ уже отменён",
            )

        await self._restore_stock(
            order,
        )

        order.status = OrderStatus.CANCELLED
        await self.db.commit()
        return await self._get_order_or_404(
            order.id,
        )

    async def get_all_orders_admin(
        self,
    ) -> list[Order]:
        result = await self.db.scalars(
            select(Order)
            .options(
                selectinload(Order.items),
            )
            .order_by(
                Order.created_at.desc(),
            )
        )
        return list(result.all())

    async def get_order_by_id_admin(
        self,
        order_id: int,
    ) -> Order:
        return await self._get_order_or_404(
            order_id,
        )

    async def change_order_status_admin(
        self,
        order_id: int,
        new_status: OrderStatus,
    ) -> Order:
        order = await self._get_order_or_404(
            order_id,
        )

        if order.status in {
            OrderStatus.COMPLETED,
            OrderStatus.CANCELLED,
        }:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Нельзя изменить финальный статус",
            )

        if order.status == new_status:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Заказ уже имеет такой статус",
            )

        if not self._is_valid_transition(
            order.status,
            new_status,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Нельзя изменить статус "
                    f"с {order.status.value} на {new_status.value}"
                ),
            )

        if new_status == OrderStatus.CANCELLED:
            await self._restore_stock(
                order,
            )
        order.status = new_status
        await self.db.commit()
        return await self._get_order_or_404(
            order.id,
        )