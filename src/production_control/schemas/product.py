from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    unique_code: str
    shift_task_id: int
    is_aggregated: bool = False
    aggregated_at: Optional[datetime] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductAggregationRequest(BaseModel):
    shift_task_id: int
    unique_code: str
