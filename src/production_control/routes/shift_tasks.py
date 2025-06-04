from datetime import date
from fastapi import APIRouter, Depends
from typing import List, Optional

from src.production_control.dependencies.dependencies import get_task_service
from src.production_control.models.shift_task import ShiftTaskCreate, ShiftTaskOut, ShiftTaskUpdate, ShiftTaskWithProductsSchema
from src.production_control.services.shift_task import ShiftTaskService

router = APIRouter(
    prefix="/shift-tasks",
    tags=["Shift Tasks"]
)



# @router.get("/books", response_model=list[BookSchema])
# async def get_books(author: Optional[str] = None, 
#                     genre: Optional[str] = None, 
#                     skip: int = 0,
#                     limit: int = 100,
#                     service: ServiceBook  = Depends(get_book_service)):

#     return await service.get_all(author, genre, skip, limit)

@router.get("/", response_model=List[ShiftTaskOut])
async def get_tasks_filter( is_closed: Optional[bool] = None,
                            batch_number: Optional[int] = None,
                            batch_date: Optional[date] = None,
                            skip: int = 0,
                            limit: int = 100,
                            service: ShiftTaskService = Depends(get_task_service)):
    

    return await service.filter(
    is_closed=is_closed,
    batch_number=batch_number,
    batch_date=batch_date,
    skip=skip,
    limit=limit
    )

@router.post("/", response_model=List[ShiftTaskOut])
async def add_shift_tasks(tasks: List[ShiftTaskCreate], service: ShiftTaskService = Depends(get_task_service)):
    return await service.add(tasks)

@router.get("/{id}", response_model=ShiftTaskWithProductsSchema)
async def get_shift_task_by_id(id: int, service: ShiftTaskService = Depends(get_task_service)):
    return await service.get_shift_tasks_by_id(id)

@router.put("/{id}", response_model=ShiftTaskOut)
async def update_shift_task_by_id(id: int, shift_task: ShiftTaskUpdate, service: ShiftTaskService = Depends(get_task_service)):
    return await service.update_shift_task_by_id(id, shift_task)
