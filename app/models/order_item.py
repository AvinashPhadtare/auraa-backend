from sqlmodel import SQLModel, Field
from sqlmodel import Relationship
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.models.order import Order


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None,primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    dish_id: int = Field(foreign_key="dish.id")
    quantity: int = Field(ge=1)
    price_at_time: int = Field(ge=0)
    dish_name_at_time: str


    order: Optional["Order"] = Relationship(back_populates="items")