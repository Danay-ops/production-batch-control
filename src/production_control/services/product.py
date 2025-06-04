


from typing import List
from src.production_control.repository.abstract_product import AbstractProductRepository


class ProductService:
    def __init__(self, repo: AbstractProductRepository) -> None:
        self.repo = repo

    async def add_product_from_raw(self, data: list[dict]) -> List:
        return await self.repo.add_product_from_raw(data)
    
    async def aggregate_product(self, shift_task_id: int, unique_code: str) -> str:
        return await self.repo.aggregate_product(shift_task_id, unique_code)