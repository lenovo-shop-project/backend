import pytest
from app.main import app
from app.security import get_current_user
from app.models.user import User
from app.models.user import UserRole


@pytest.mark.asyncio
async def test_add_product_requires_admin(async_client):
    product_payload = {
        "name": "Lenovo ThinkPad X1",
        "description": "Топовый ноутбук для разработчиков",
        "price": 75000,
        "stock": 10,
        "category_id": 1
    }

    # 1 Проверка того что меня не пустит без админа
    response_no_auth = await async_client.post("/admin/products", json=product_payload)
    assert response_no_auth.status_code in [401, 403]

    # 2 "Цыганские фокусы" (функция заглушка с фейковым админом)
    async def override_get_current_user():
        return User(id=999, email="admin@test.com", role=UserRole.ADMIN)

    # 3 Подмена на заглушку
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        # СНАЧАЛА создание категории
        cat_payload = {"name": "Ноутбуки", "description": "Тестовая категория"}
        cat_res = await async_client.post("/admin/categories", json=cat_payload)
        assert cat_res.status_code == 201, f"Ошибка создания категории: {cat_res.json()}"
        
        # Получаем ID только что созданной категории
        category_id = cat_res.json()["id"]

        # Обновляем payload товара правильным ID
        product_payload["category_id"] = category_id

        # Теперь делаем запрос от "админа" на создание товара
        response_with_auth = await async_client.post("/admin/products", json=product_payload)
        
        # ожидание 201 Created
        assert response_with_auth.status_code == 201, f"Ошибка создания товара: {response_with_auth.json()}"
        assert response_with_auth.json()["name"] == "Lenovo ThinkPad X1"
    finally:
        # ОЧЕНЬ ВАЖНО: удаляем подмену после теста
        del app.dependency_overrides[get_current_user]