from sqlmodel import Session
from fastapi import HTTPException
from app.crud import order as order_crud 
from app.schemas.bill import BillResponse
from app.schemas.order import OrderItemResponse, OrderResponse
from app.models.order import OrderStatus

def get_bill(session: Session, order_id: int):
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    item_responses = [
        OrderItemResponse(
        dish_name=item.dish_name_at_time,
        quantity=item.quantity,
        price_at_time=item.price_at_time
        )
    for item in order.items
    ]
    qr_code_url = f"/static/qr/{order.id}.png"

    return BillResponse(
        order_id=order.id,
        items=item_responses,
        total_amount=order.total_amount,
        qr_code_url=qr_code_url,
        status=order.status.value
    )

def confirm_payment(session:Session, order_id:int):
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == OrderStatus.paid:
        raise HTTPException(status_code=400, detail="Order is already paid")
    updated_order = order_crud.update_order_status(session, order, OrderStatus.paid)
    item_responses = [
    OrderItemResponse(
        dish_name=item.dish_name_at_time,
        quantity=item.quantity,
        price_at_time=item.price_at_time
    )
    for item in updated_order.items
    ]
    return OrderResponse(
        id=updated_order.id,
        total_amount=updated_order.total_amount,
        status=updated_order.status.value,
        created_at=updated_order.created_at,
        table_number=order.table_number,
        items=item_responses
    )
