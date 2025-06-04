from datetime import date
from typing import Optional

from fastapi import HTTPException
from src.production_control.models.shift_task import ShiftTaskCreate, ShiftTaskOut, ShiftTaskUpdate
from src.production_control.repository.abstract_shift_task import AbstractShiftTaskRepository


class ShiftTaskService:
    def __init__(self, repo: AbstractShiftTaskRepository) -> None:
        self.repo = repo

    async def add(self, tasks: list[ShiftTaskCreate]) -> None:
        return await self.repo.add_shift_task(tasks)
    
    async def get_shift_tasks_by_id(self, id: int) -> Optional[ShiftTaskOut]:
        res = await self.repo.get_shift_tasks_by_id(id)
        if res is None:
            raise HTTPException(status_code=404, detail=f"Задание с id {id} не найдено")
        return res
    
    async def update_shift_task_by_id(self, id: int, shift_task: ShiftTaskUpdate) -> ShiftTaskOut:
        res = await self.repo.update_shift_task_by_id(id, shift_task)
        if res is None:
            raise HTTPException(status_code=404, detail=f"Задание с id {id} не найдено")
        return res
    
    async def filter(
        self,
        is_closed: Optional[bool] = None,
        batch_number: Optional[int] = None,
        batch_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ShiftTaskOut]:
        
        if is_closed is None:
            is_closed = True

        tasks = await self.repo.filter(
            is_closed=is_closed,
            batch_number=batch_number,
            batch_date=batch_date,
            skip=skip,
            limit=limit
        )

        return [ShiftTaskOut.model_validate(task) for task in tasks]

