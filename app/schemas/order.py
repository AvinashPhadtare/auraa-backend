from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import List
from datetime import datetime

class OrderItemInput(BaseModel):
    dish_id: int = Field(ge=1)
    quantity: int = Field(ge=1)

class OrderCreate(BaseModel):
    table_number: str | None = None
    items: List[OrderItemInput] = Field(min_length=1)

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    dish_name: str
    quantity: int 
    price_at_time: int  
    @computed_field
    @property
    def subtotal(self) -> int:
        return self.price_at_time * self.quantity

class OrderResponse(BaseModel):
    id: int
    total_amount: int
    status: str
    created_at: datetime
    table_number: str | None = None
    items: List[OrderItemResponse]
    model_config = ConfigDict(from_attributes=True)
