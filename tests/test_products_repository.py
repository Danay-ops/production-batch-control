import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import NullPool, text
from src.production_control.main import app
from httpx import AsyncClient
from src.production_control.db.session import get_db
from src.production_control.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker



@pytest.mark.asyncio
async def test_add_products_endpoint():
    # Сначала создадим shift_task, к которому привяжем продукт
    shift_task_data = {
        "is_closed": True,
        "task_name": "тест_для_продуктов",
        "work_center": "string",
        "shift": "string",
        "brigade": "string",
        "batch_number": 12345,
        "batch_date": "2024-01-30",
        "nomenclature": "string",
        "ekn_code": "string",
        "rc_id": "string",
        "start_shift_time": "2024-01-30T08:00:00",
        "end_shift_time": "2024-01-30T16:00:00"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем shift_task через API (предполагаем, что у тебя есть эндпоинт /shift-tasks/)
        post_task_resp = await client.post("/shift-tasks/", json=[shift_task_data])
        assert post_task_resp.status_code == 200
        task_id = post_task_resp.json()[0]["id"]

        # Подготовим данные продуктов
        products_data = [
            {
                "УникальныйКодПродукта": "code_123",
                "НомерПартии": 12345,
                "ДатаПартии": "2024-01-30"
            },
            {
                "УникальныйКодПродукта": "code_456",
                "НомерПартии": 99999,  # такой партии нет
                "ДатаПартии": "2024-01-31"
            },
            {
                "УникальныйКодПродукта": "code_123",  # дубликат
                "НомерПартии": 12345,
                "ДатаПартии": "2024-01-30"
            }
        ]


        # Отправляем продукцию
        post_products_resp = await client.post("/products/", json=products_data)
        assert post_products_resp.status_code == 200
        added_codes = post_products_resp.json()
        # Проверяем, что добавлен только уникальный код с существующей партией
        assert added_codes == ["code_123"]


        # Получаем shift_task с продуктами и проверяем
        get_task_resp = await client.get(f"/shift-tasks/{task_id}")
        assert get_task_resp.status_code == 200
        task_with_products = get_task_resp.json()

        # Проверяем, что products содержит только добавленные уникальные коды
        assert "code_123" in task_with_products["products"]
        # Можно дополнительно проверить, что там нет кода с несуществующей партией или дубликата
        assert "code_456" not in task_with_products["products"]





@pytest.mark.asyncio
async def test_aggregate_product_endpoint():
    # Создаем shift_task
    shift_task_data = {
        "is_closed": True,
        "task_name": "тест агрегации",
        "work_center": "string",
        "shift": "string",
        "brigade": "string",
        "batch_number": 12345,
        "batch_date": "2024-01-30",
        "nomenclature": "string",
        "ekn_code": "string",
        "rc_id": "string",
        "start_shift_time": "2024-01-30T08:00:00",
        "end_shift_time": "2024-01-30T16:00:00"
    }

    product_data = {
        "УникальныйКодПродукта": "unique_code_test",
        "НомерПартии": 12345,
        "ДатаПартии": "2024-01-30"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем сменное задание
        task_resp = await client.post("/shift-tasks/", json=[shift_task_data])
        assert task_resp.status_code == 200
        shift_task_id = task_resp.json()[0]["id"]

        # Добавляем продукт
        prod_resp = await client.post("/products/", json=[product_data])
        assert prod_resp.status_code == 200

        # 1. Успешная агрегация
        agg_resp = await client.post("/products/aggregate", json={
            "shift_task_id": shift_task_id,
            "unique_code": "unique_code_test"
        })
        assert agg_resp.status_code == 200
        assert agg_resp.json() == "unique_code_test"

        # 2. Повторная агрегация — ошибка 400 с сообщением
        agg_resp_repeat = await client.post("/products/aggregate", json={
            "shift_task_id": shift_task_id,
            "unique_code": "unique_code_test"
        })
        assert agg_resp_repeat.status_code == 400
        assert "already used" in agg_resp_repeat.json()["detail"]

        # 3. Аггрегация продукта с правильным кодом, но неправильным shift_task_id — ошибка 400
        agg_resp_wrong_batch = await client.post("/products/aggregate", json={
            "shift_task_id": shift_task_id + 9999,
            "unique_code": "unique_code_test"
        })
        assert agg_resp_wrong_batch.status_code == 400
        assert "attached to another batch" in agg_resp_wrong_batch.json()["detail"]

        # 4. Аггрегация несуществующего уникального кода — ошибка 404
        agg_resp_not_found = await client.post("/products/aggregate", json={
            "shift_task_id": shift_task_id,
            "unique_code": "nonexistent_code"
        })
        assert agg_resp_not_found.status_code == 404
        assert agg_resp_not_found.json()["detail"] == "unique code not found"