# from datetime import date, datetime
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from typing import Optional
# from sqlalchemy.orm import relationship
# from src.production_control.db.base import Base
# from sqlalchemy import ForeignKey
# from typing import Optional



# class Product(Base):
#     __tablename__ = 'products'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     unique_code: Mapped[str] = mapped_column(unique=True, index=True)
#     shift_task_id: Mapped[str] = mapped_column(ForeignKey("shift_tasks.id"))

#     is_aggregated: Mapped[bool] = mapped_column(default=False)
#     aggregated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

#     shift_task: Mapped["ShiftTasks"] = relationship(back_populates="products")


from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.production_control.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_code: Mapped[str] = mapped_column(unique=True, nullable=False)  # <-- уникальный код
    is_aggregated: Mapped[bool] = mapped_column(default=False)
    aggregated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    shift_task_id: Mapped[int] = mapped_column(ForeignKey("shift_tasks.id"), nullable=False)

    shift_task: Mapped["ShiftTasks"] = relationship(
        "ShiftTasks",
        back_populates="products"
    )

