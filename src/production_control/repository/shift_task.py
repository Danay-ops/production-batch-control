from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from typing import Optional
from src.production_control.db.shift_tasks import ShiftTasks
from src.production_control.models.shift_task import ShiftTaskCreate, ShiftTaskOut, ShiftTaskUpdate, ShiftTaskWithProductsSchema
from src.production_control.repository.abstract_shift_task import AbstractShiftTaskRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ShiftTaskRepository(AbstractShiftTaskRepository):
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_shift_task(self, tasks: list[ShiftTaskCreate]) -> list[ShiftTaskOut]:
        # db_tasks = [ShiftTasks(**task.dict()) for task in tasks]
        db_tasks = [ShiftTasks(**task.model_dump()) for task in tasks]

        self.session.add_all(db_tasks)
        await self.session.commit()
        for task in db_tasks:
            await self.session.refresh(task)

        return [ShiftTaskOut.model_validate(task) for task in db_tasks]
    
    async def get_shift_tasks_by_id(self, id: int) -> Optional[ShiftTaskWithProductsSchema]:
        result = await self.session.execute(
            select(ShiftTasks)
            .options(selectinload(ShiftTasks.products))
            .where(ShiftTasks.id == id)
        )
        task = result.scalars().first()
        if not task:
            return None
        
        # Формируем список уникальных кодов продукции
        product_codes = [product.unique_code for product in task.products]

        # Возвращаем объект, соответствующий схеме с products
        return ShiftTaskWithProductsSchema(
            id=task.id,
            is_closed=task.is_closed,
            task_name=task.task_name,
            work_center=task.work_center,
            shift=task.shift,
            brigade=task.brigade,
            batch_number=task.batch_number,
            batch_date=task.batch_date,
            nomenclature=task.nomenclature,
            ekn_code=task.ekn_code,
            rc_id=task.rc_id,
            start_shift_time=task.start_shift_time,
            end_shift_time=task.end_shift_time,
            products=product_codes
        )
        

    async def get_shift_task_orm_by_id(self, id: int) -> Optional[ShiftTasks]:
        result = await self.session.execute(
            select(ShiftTasks)
            .options(selectinload(ShiftTasks.products))
            .where(ShiftTasks.id == id)
        )
        return result.scalars().first()


    async def update_shift_task_by_id(self, id: int, shift_task: ShiftTaskUpdate):
        task = await self.get_shift_task_orm_by_id(id)
        if task is None:
            return None

        task.is_closed = shift_task.is_closed
        task.task_name = shift_task.task_name
        task.work_center = shift_task.work_center
        task.shift = shift_task.shift
        task.brigade = shift_task.brigade
        task.batch_number = shift_task.batch_number
        task.batch_date = shift_task.batch_date
        task.nomenclature = shift_task.nomenclature
        task.ekn_code = shift_task.ekn_code
        task.rc_id = shift_task.rc_id
        task.start_shift_time = shift_task.start_shift_time
        task.end_shift_time = shift_task.end_shift_time

        await self.session.commit()
        await self.session.refresh(task)

        return ShiftTaskOut.model_validate(task)

    async def filter(
    self,
    is_closed: Optional[bool] = None,
    batch_number: Optional[int] = None,
    batch_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ShiftTasks]:
        stmt = select(ShiftTasks)

        if is_closed is not None:
            stmt = stmt.where(ShiftTasks.is_closed == is_closed)
        if batch_number is not None:
            stmt = stmt.where(ShiftTasks.batch_number == batch_number)
        if batch_date is not None:
            stmt = stmt.where(ShiftTasks.batch_date == batch_date)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()