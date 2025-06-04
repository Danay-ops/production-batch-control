from abc import ABC, abstractmethod
from typing import Optional

from src.production_control.models.shift_task import ShiftTaskBase, ShiftTaskCreate, ShiftTaskOut, ShiftTaskUpdate


class AbstractShiftTaskRepository(ABC):

    @abstractmethod
    async def add_shift_task(self, tasks: list[ShiftTaskCreate]) -> None:
        pass

    @abstractmethod
    async def get_shift_tasks_by_id(self, id: int) -> Optional[ShiftTaskOut]:
        pass

    @abstractmethod
    async def update_shift_task_by_id(self, id: int, shift_task: ShiftTaskUpdate) -> ShiftTaskOut:
        pass

    @abstractmethod
    async def filter(self, **kwargs) -> list[ShiftTaskOut]:
        pass