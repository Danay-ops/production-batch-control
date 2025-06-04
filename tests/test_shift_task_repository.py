import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import NullPool, text
from src.production_control.main import app
from httpx import AsyncClient
from src.production_control.db.session import get_db
from src.production_control.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


# DATABASE_TEST_URL = "postgresql+asyncpg://user:password@db:5432/testdb_for_test"

# # Создаём движок специально для тестов
# test_engine = create_async_engine(DATABASE_TEST_URL, poolclass=NullPool)
# TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

# # Переопределим зависимость
# async def override_get_db():
#     async with TestSessionLocal() as session:
#         yield session

# app.dependency_overrides[get_db] = override_get_db

# # Перед запуском тестов создаём таблицы
# @pytest.fixture(scope="session", autouse=True)
# async def prepare_test_db():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(autouse=True)
# def clean_tables_fixture():
#     """Синхронная фикстура, вызывающая асинхронную функцию очистки таблиц."""
#     yield  # дожидаемся завершения теста

#     async def truncate():
#         async with test_engine.begin() as conn:
#             tables = await conn.run_sync(lambda sync_conn: list(Base.metadata.tables.keys()))
#             for table in tables:
#                 await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))

#     asyncio.run(truncate())


@pytest.mark.asyncio
async def test_shift_task_repository():
    task_data = [
        {
            "is_closed": True,
            "task_name": "крниж_test_shift_task_repository",
            "work_center": "string",
            "shift": "string",
            "brigade": "string",
            "batch_number": 3,
            "batch_date": "2025-06-05",
            "nomenclature": "string",
            "ekn_code": "string",
            "rc_id": "string",
            "start_shift_time": "2025-06-05T08:08:02",
            "end_shift_time": "2025-06-05T08:08:02"
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/shift-tasks/", json=task_data)
        assert response.status_code == 200
        data = response.json()
        assert data[0]["task_name"] == 'крниж_test_shift_task_repository'

@pytest.mark.asyncio
async def test_get_shift_task_by_id():
    task_data = [
        {
            "is_closed": True,
            "task_name": "крниж_тест_get_shift_task_by_id",
            "work_center": "string",
            "shift": "string",
            "brigade": "string",
            "batch_number": 3,
            "batch_date": "2025-06-05",
            "nomenclature": "string",
            "ekn_code": "string",
            "rc_id": "string",
            "start_shift_time": "2025-06-05T08:08:02",
            "end_shift_time": "2025-06-05T08:08:02"
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as client:
        post_response = await client.post("/shift-tasks/", json=task_data)
        assert post_response.status_code == 200
        task_id = post_response.json()[0]["id"]

        get_response = await client.get(f"/shift-tasks/{task_id}")
        assert get_response.status_code == 200
        result = get_response.json()

        assert result["task_name"] == "крниж_тест_get_shift_task_by_id"
        assert isinstance(result["products"], list)
        assert result["products"] == []




@pytest.mark.asyncio
async def test_update_shift_task_by_id():
    
    task_data   =                               {
                    "is_closed": True,
                    "task_name": "test_update_shift_task_by_id",
                    "work_center": "string",
                    "shift": "string",
                    "brigade": "string",
                    "batch_number": 0,
                    "batch_date": "2025-06-04",
                    "nomenclature": "string",
                    "ekn_code": "string",
                    "rc_id": "string",
                    "start_shift_time": "2025-06-04T12:21:01",
                    "end_shift_time": "2025-06-04T12:21:01"
                    }
        
    
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        post_response = await client.post("/shift-tasks/", json=[task_data])
        assert post_response.status_code == 200
        task_id = post_response.json()[0]["id"]

        update_data  = {
                "is_closed": True,
                "task_name": "test_update_shift_task_by_id_updated",
                "work_center": "center2",
                "shift": "night",
                "brigade": "string",
                "batch_number": 0,
                "batch_date": "2025-06-04",
                "nomenclature": "string",
                "ekn_code": "string",
                "rc_id": "string",
                "start_shift_time": "2025-06-04T12:21:01",
                "end_shift_time": "2025-06-04T12:21:01"
                }

        put_resp = await client.put(f"/shift-tasks/{task_id}", json=update_data)
        assert put_resp.status_code == 200
        updated_task = put_resp.json()

        assert updated_task["task_name"] == "test_update_shift_task_by_id_updated"
        assert updated_task["work_center"] == "center2"
        assert updated_task["shift"] == "night"
        # Проверяем, что остальные поля остались без изменений
        assert updated_task["brigade"] == task_data["brigade"]
        assert updated_task["is_closed"] == task_data["is_closed"]





@pytest.mark.asyncio
async def test_get_tasks_filter():  
    tasks = [
        {
            "is_closed": True,
            "task_name": "Task 1",
            "work_center": "WC1",
            "shift": "morning",
            "brigade": "brig1",
            "batch_number": 1,
            "batch_date": "2025-06-01",
            "nomenclature": "nom1",
            "ekn_code": "code1",
            "rc_id": "rc1",
            "start_shift_time": "2025-06-01T08:00:00",
            "end_shift_time": "2025-06-01T16:00:00"
        },
        {
            "is_closed": False,
            "task_name": "Task 2",
            "work_center": "WC2",
            "shift": "evening",
            "brigade": "brig2",
            "batch_number": 2,
            "batch_date": "2025-06-02",
            "nomenclature": "nom2",
            "ekn_code": "code2",
            "rc_id": "rc2",
            "start_shift_time": "2025-06-02T16:00:00",
            "end_shift_time": "2025-06-02T00:00:00"
        },
        {
            "is_closed": True,
            "task_name": "Task 3",
            "work_center": "WC3",
            "shift": "night",
            "brigade": "brig3",
            "batch_number": 1,
            "batch_date": "2025-06-02",
            "nomenclature": "nom3",
            "ekn_code": "code3",
            "rc_id": "rc3",
            "start_shift_time": "2025-06-01T00:00:00",
            "end_shift_time": "2025-06-01T08:00:00"
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаём записи в базе через POST эндпоинт
        
        response = await client.post("/shift-tasks/", json=tasks)
        assert response.status_code == 200

        # Теперь тестируем фильтрацию по is_closed=True
        resp = await client.get("/shift-tasks/?is_closed=true")
        assert resp.status_code == 200
        data = resp.json()
        assert all(task["is_closed"] is True for task in data)
        assert len(data) == 2  # Task 1 и Task 3

        # Фильтрация по batch_number=1
        resp = await client.get("/shift-tasks/?batch_number=1")
        assert resp.status_code == 200
        data = resp.json()
        assert all(task["batch_number"] == 1 for task in data)
        assert len(data) == 2  # Task 1 и Task 3

        # Фильтрация по batch_date=2025-06-02
        resp = await client.get("/shift-tasks/?batch_date=2025-06-02")
        assert resp.status_code == 200
        data = resp.json()
        assert all(task["batch_date"] == "2025-06-02" for task in data)
        assert len(data) == 1  # Task 2

        # Тест пагинации limit=1, skip=1
        resp = await client.get("/shift-tasks/?limit=1&skip=1")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1  # возвращается ровно 1 задача
