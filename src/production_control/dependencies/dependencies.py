from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession




from src.production_control.services.product import ProductService
from src.production_control.repository.product import ProductRepository
from src.production_control.repository.abstract_product import AbstractProductRepository
from src.production_control.db.session import get_db
from src.production_control.repository.abstract_shift_task import AbstractShiftTaskRepository
from src.production_control.repository.shift_task import ShiftTaskRepository
from src.production_control.services.shift_task import ShiftTaskService



def get_shift_task_repo(session: AsyncSession = Depends(get_db)) -> AbstractShiftTaskRepository:
    return ShiftTaskRepository(session)


def get_task_service(repo: AbstractShiftTaskRepository = Depends(get_shift_task_repo)):
    return ShiftTaskService(repo)

def get_product_repo(session: AsyncSession = Depends(get_db)) -> AbstractProductRepository:
    return ProductRepository(session)

def get_product_service(repo: AbstractProductRepository = Depends(get_product_repo)) -> ProductService:
    return ProductService(repo)