from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

class ShiftTaskBase(BaseModel):
    is_closed: bool
    task_name: str
    work_center: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    ekn_code: str
    rc_id: str
    start_shift_time: datetime
    end_shift_time: datetime

class ShiftTaskCreate(ShiftTaskBase):
    pass

class ShiftTaskUpdate(BaseModel):
    is_closed: Optional[bool] = None
    task_name: Optional[str] = None
    work_center: Optional[str] = None
    shift: Optional[str] = None
    brigade: Optional[str] = None
    batch_number: Optional[int] = None
    batch_date: Optional[date] = None
    nomenclature: Optional[str] = None
    ekn_code: Optional[str] = None
    rc_id: Optional[str] = None
    start_shift_time: Optional[datetime] = None
    end_shift_time: Optional[datetime] = None

class ShiftTaskOut(ShiftTaskBase):
    id: int

    class Config:
        from_attributes = True

class ShiftTaskWithProductsSchema(BaseModel):
    id: int
    is_closed: bool
    task_name: str
    work_center: str
    shift: str
    brigade: str
    batch_number: int
    batch_date: date
    nomenclature: str
    ekn_code: str
    rc_id: str
    start_shift_time: datetime
    end_shift_time: datetime
    products: List[str]  

    class Config:
        orm_mode = True