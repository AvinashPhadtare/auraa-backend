from sqlmodel import Session 
from fastapi import HTTPException
from app.crud import order as order_crud
from app.crud import dish as dish_crud
from app.schemas.order import OrderCreate
from app.schemas.bill import BillResponse
from app.schemas.order import OrderItemResponse
from app.utils.qr_generator import generate_qr


def place_order(session:Session, order_data:OrderCreate):
    items_data = []
    for item in order_data.items:
        dish = dish_crud.get_dish_by_id(session, item.dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish with id {item.dish_id} not found")
        price_at_time = dish.price
        dish_name_at_time = dish.dish_name
        subtotal = price_at_time * item.quantity
        items_data.append({
            "dish_id": item.dish_id,
            "quantity": item.quantity,
            "price_at_time": price_at_time,
            "dish_name_at_time": dish_name_at_time,
            "subtotal": subtotal
        })
    total_amount = sum(item["subtotal"] for item in items_data)
    order = order_crud.create_order(session, total_amount, items_data, order_data.table_number)
    try:
        qr_path = generate_qr(order.id, total_amount)
        order_crud.update_order_qr_path(session, order, qr_path)
    except Exception:
        pass
    qr_code_url = f"/static/qr/{order.id}.png"
    item_responses = [
    OrderItemResponse(
        dish_name=item["dish_name_at_time"],
        quantity=item["quantity"],
        price_at_time=item["price_at_time"]
    )
    for item in items_data
    ]
    return BillResponse(
        order_id=order.id,
        items=item_responses,
        total_amount=total_amount,
        qr_code_url=qr_code_url,
        status=order.status.value
    )
    
def delete_order(session: Session, order_id: int):
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order_crud.delete_order(session, order)
    return {"message": f"Order #{order_id} deleted successfully"}