



from abc import ABC, abstractmethod
from typing import List



class AbstractProductRepository(ABC):

    @abstractmethod
    async def add_product_from_raw(self, data: list[dict]) -> List:
        """Добавление продукции на основе входных данных из системы"""
        pass

    @abstractmethod
    async def aggregate_product(self, shift_task_id: int, unique_code: str) -> str:
        """Агрегация продукции по коду и ID сменного задания.
        Возвращает уникальный код если успешно, иначе вызывает исключения"""
        pass