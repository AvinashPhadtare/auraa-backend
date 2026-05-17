from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.services import dish_service as service
from app.db.session import get_session
from app.schemas.dish import DishResponse


router = APIRouter()

@router.get("/menu")
def show_menu(session: Session = Depends(get_session)):
    result = service.get_all_dishes(session)
    
    return result