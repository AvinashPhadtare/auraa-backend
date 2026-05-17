from sqlmodel import SQLModel, Field
from typing import TYPE_CHECKING,List
if TYPE_CHECKING:
    from app.models.order_item import OrderItem
from datetime import datetime,timezone
from sqlmodel import Relationship
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    total_amount: int = Field(ge=0)
    status: OrderStatus = OrderStatus.pending
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))
    qr_code_path: str | None = Field(default=None)
    table_number: str | None = Field(default=None)

    items: List["OrderItem"] = Relationship(back_populates="order")
