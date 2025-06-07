from fastapi import FastAPI
from src.production_control.db.session import engine, Base
from src.production_control.routes import shift_tasks, products

from src.production_control.db.base import Base

# ВАЖНО: импорт моделей
from production_control.db.models.shift_tasks import ShiftTasks
from production_control.db.models.product import Product



from src.production_control.routes.shift_tasks import router as shift_tasks
from src.production_control.routes.products import router as products



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(shift_tasks)
app.include_router(products)
