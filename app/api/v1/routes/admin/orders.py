from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from datetime import datetime, timezone, timedelta
from typing import Optional
from app.db.session import get_session
from app.api.deps import get_current_admin
from app.crud import order as order_crud
from app.schemas.order import OrderResponse, OrderItemResponse

router = APIRouter()

def build_order_responses(orders):
    result = []
    for order in orders:
        item_responses = [
            OrderItemResponse(
                dish_name=item.dish_name_at_time,
                quantity=item.quantity,
                price_at_time=item.price_at_time
            )
            for item in order.items
        ]
        order_response = OrderResponse(
            id=order.id,
            total_amount=order.total_amount,
            status=order.status.value,
            created_at=order.created_at,
            table_number=order.table_number,
            items=item_responses
        )
        result.append(order_response)
    return result


@router.get("/")
def get_all_paid_orders(
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin),
    filter: Optional[str] = Query(default=None)
):
    now = datetime.now(timezone.utc)

    if filter == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif filter == "week":
        start = now - timedelta(days=7)
        end = now
    elif filter == "month":
        start = now - timedelta(days=30)
        end = now
    else:
        orders = order_crud.get_paid_orders(session)
        return build_order_responses(orders)

    orders = order_crud.get_orders_by_date(session, start, end)
    return build_order_responses(orders)


@router.get("/{order_id}")
def get_order_detail(order_id: int, session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    order = order_crud.get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return build_order_responses([order])[0]
    

@router.delete("/{order_id}")
def delete_order(order_id: int, session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    from app.services import order_service
    result = order_service.delete_order(session, order_id)
    return result