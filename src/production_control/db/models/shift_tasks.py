# from datetime import date, datetime
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from typing import TYPE_CHECKING, List
# from typing import List, Optional
# from sqlalchemy.orm import relationship
# from src.production_control.db.base import Base

# if TYPE_CHECKING:
#     from src.production_control.db.product import Product


# class ShiftTasks(Base):
#     __tablename__ = "shift_tasks"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     is_closed: Mapped[bool] = mapped_column(default=False)
#     task_name: Mapped[str]  
#     work_center: Mapped[str]
#     shift: Mapped[str]
#     brigade: Mapped[str]
#     batch_number: Mapped[int]
#     batch_date: Mapped[date]
#     nomenclature: Mapped[str]
#     ekn_code: Mapped[str]
#     rc_id: Mapped[str]
#     start_shift_time: Mapped[datetime]
#     end_shift_time: Mapped[datetime]

#     products: Mapped[List["Product"]] = relationship(
#         "Product",
#         back_populates="shift_task",
#         cascade="all, delete-orphan"
#     )


from datetime import date, datetime
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.production_control.db.base import Base

if TYPE_CHECKING:
    from production_control.db.models.product import Product

class ShiftTasks(Base):
    __tablename__ = "shift_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_closed: Mapped[bool] = mapped_column(default=False)
    task_name: Mapped[str]
    work_center: Mapped[str]
    shift: Mapped[str]
    brigade: Mapped[str]
    batch_number: Mapped[int]
    batch_date: Mapped[date]
    nomenclature: Mapped[str]
    ekn_code: Mapped[str]
    rc_id: Mapped[str]
    start_shift_time: Mapped[datetime]
    end_shift_time: Mapped[datetime]

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="shift_task",
        cascade="all, delete-orphan"
    )
