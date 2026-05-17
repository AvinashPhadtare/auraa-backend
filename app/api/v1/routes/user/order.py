from fastapi import APIRouter, Depends 
from sqlmodel import Session 
from app.db.session import get_session 
from app.services import order_service
from app.services import bill_service
from app.schemas.order import OrderCreate

router = APIRouter()

@router.post("/")
def place_order(order_data: OrderCreate, session: Session = Depends(get_session)):
    result = order_service.place_order(session, order_data)
    return result

@router.get("/{order_id}/bill")
def get_bill(order_id: int, session: Session = Depends(get_session)):
    result = bill_service.get_bill(session, order_id)
    return result

@router.post("/{order_id}/pay")
def confirm_payment(order_id: int, session: Session = Depends(get_session)):
    result = bill_service.confirm_payment(session, order_id)
    return result