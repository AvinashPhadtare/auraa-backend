from datetime import datetime
from sqlmodel import Session, select
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.order import OrderStatus
from typing import List

def create_order(session: Session, total_amount: int, items_data: list, table_number: str | None = None):
    order = Order(total_amount=total_amount, table_number=table_number)
    session.add(order)
    session.commit()
    session.refresh(order)
    for item in items_data:
        order_item = OrderItem(
            order_id=order.id,
            dish_id=item["dish_id"],
            quantity=item["quantity"],
            price_at_time=item["price_at_time"],
            dish_name_at_time=item["dish_name_at_time"])
        session.add(order_item)
    
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session:Session, order_id: int):
    order = session.get(Order, order_id)
    
    return order
    
    

def get_paid_orders(session:Session):
    list_of_orders = session.exec(select(Order).where(Order.status == OrderStatus.paid)).all()

    return list_of_orders

def update_order_status(session:Session, order:Order, new_status:OrderStatus):
    order.status = new_status
    session.commit()
    session.refresh(order)
    
    return order

def update_order_qr_path(session:Session, order:Order, qr_path: str):
    order.qr_code_path = qr_path
    session.commit()
    session.refresh(order)

    return order

def delete_order(session: Session, order: Order):
    for item in order.items:
        session.delete(item)
    session.delete(order)
    session.commit()


def get_orders_by_date(session: Session, start_date: datetime, end_date: datetime):
    list_of_orders = session.exec(
        select(Order).where(
            Order.status == OrderStatus.paid,
            Order.created_at >= start_date,
            Order.created_at <= end_date
        )
    ).all()
    return list_of_orders