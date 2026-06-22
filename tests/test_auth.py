import pytest

@pytest.mark.asyncio
async def test_token_and_role_check(async_client):
    user_data = {"email": "admin@lenovo.ua", "password": "strongpassword123", "username": "admin"}
    
    reg_res = await async_client.post("/auth/register", json=user_data)
    assert reg_res.status_code == 201, f"Ошибка регистрации: {reg_res.json()}"
    
    login_res = await async_client.post("/auth/login", json={"email": "admin@lenovo.ua", "password": "strongpassword123"})
    assert login_res.status_code == 200, f"Ошибка логина: {login_res.json()}"
    
    token = login_res.json()["access_token"]

    # Проверка токена и роли
    headers = {"Authorization": f"Bearer {token}"}
    me_response = await async_client.get("/auth/me", headers=headers)
    
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@lenovo.ua"