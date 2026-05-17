from pydantic import BaseModel
from typing import List
from app.schemas.order import OrderItemResponse

class BillResponse(BaseModel):
    order_id: int
    items: List[OrderItemResponse]
    total_amount: int
    qr_code_url: str
    status: str
    