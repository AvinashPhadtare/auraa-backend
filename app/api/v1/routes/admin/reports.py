from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime, timezone
from app.db.session import get_session
from app.api.deps import get_current_admin
from app.crud import order as order_crud
from app.models.order_item import OrderItem

router = APIRouter()

@router.get("/daily")
def get_daily_report(
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin)
):
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = now

    orders = order_crud.get_orders_by_date(session, start, end)

    total_orders = len(orders)
    total_revenue = sum(o.total_amount for o in orders)
    avg_order_value = total_revenue // total_orders if total_orders > 0 else 0

    dish_counts: dict[str, int] = {}
    for order in orders:
        for item in order.items:
            name = item.dish_name_at_time
            dish_counts[name] = dish_counts.get(name, 0) + item.quantity

    most_ordered = max(dish_counts, key=dish_counts.get) if dish_counts else "—"

    return {
        "date": now.strftime("%Y-%m-%d"),
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "average_order_value": avg_order_value,
        "most_ordered_dish": most_ordered
    }