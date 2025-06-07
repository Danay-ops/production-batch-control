from datetime import datetime
from typing import List

from fastapi import HTTPException
from production_control.db.models.product import Product
from production_control.db.models.shift_tasks import ShiftTasks
from src.production_control.repository.abstract_product import AbstractProductRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def add_product_from_raw(self, data: list[dict]) -> List:
        added = []

        for item in data:
            unique_code = item.get('УникальныйКодПродукта')
            batch_number = item.get("НомерПартии")
            # batch_date = item.get("ДатаПартии")
            batch_date = datetime.strptime(item.get("ДатаПартии"), "%Y-%m-%d").date()

            # Проверка: уже существует такой код?
            stmt = select(Product).where(Product.unique_code == unique_code)
            result = await self.session.execute(stmt)
            if result.scalar():
                continue

            # Поиск shift_task по номеру и дате партии
            task_stmt = select(ShiftTasks).where(
                ShiftTasks.batch_number == batch_number,
                ShiftTasks.batch_date == batch_date
            )

            task_result = await self.session.execute(task_stmt)
            shift_task = task_result.scalar()
            if not shift_task:
                continue

            product = Product(
                unique_code=unique_code,
                shift_task_id=shift_task.id,
                is_aggregated=False,
                aggregated_at=None
            )
            self.session.add(product)
            added.append(unique_code)

        await self.session.commit()
        print(f"Committed products: {added}")  # <-- лог коммита
        return added

    async def aggregate_product(self, shift_task_id: int, unique_code: str) -> str:
        stmt = select(Product).where(Product.unique_code == unique_code)
        result = await self.session.execute(stmt)
        product = result.scalar()

        if not product:
            raise HTTPException(status_code=404, detail="unique code not found")

        if product.shift_task_id != shift_task_id:
            raise HTTPException(
                status_code=400,
                detail="unique code is attached to another batch"
            )
        
        if product.is_aggregated:
            raise HTTPException(
                status_code=400,
                detail=f"unique code already used at {product.aggregated_at}"
            )


        product.is_aggregated = True
        product.aggregated_at = datetime.utcnow()

        await self.session.commit()
        return product.unique_code