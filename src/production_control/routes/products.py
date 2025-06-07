from typing import List
from fastapi import APIRouter, Depends

from src.production_control.dependencies.dependencies import get_product_service
from src.production_control.schemas.product import ProductAggregationRequest, ProductOut
from src.production_control.services.product import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=List[str])
async def add_products( products_data: list[dict],
                        service: ProductService = Depends(get_product_service)):
    return await service.add_product_from_raw(products_data)

@router.post("/aggregate", response_model=str)
async def aggregate_product(
    request: ProductAggregationRequest,
    service: ProductService = Depends(get_product_service)
):
    return await service.aggregate_product(
        shift_task_id=request.shift_task_id,
        unique_code=request.unique_code
    )