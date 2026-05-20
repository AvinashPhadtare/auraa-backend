from fastapi import APIRouter, Depends,UploadFile, File,HTTPException
from sqlmodel import Session
import shutil
import os

from app.utils.cloudinary import upload_image  
from app.db.session import get_session
from app.api.deps import get_current_admin
from app.services import dish_service as service 
from app.schemas.dish import DishCreate, DishResponse, DishUpdate
from app.models.dish import Dish


router = APIRouter()


@router.post("/")
def add_dish(dish_data: DishCreate, session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    result = service.add_dish(session, dish_data)
    return result

@router.get("/")
def get_all_dishes(session:Session = Depends(get_session), admin = Depends(get_current_admin)):
    result = service.get_all_dishes(session)

    return result


@router.patch("/{dish_id}")
def update_dish(dish_id: int, new_data: DishUpdate, session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    result = service.update_dish(session, dish_id, new_data)
    return result


@router.delete("/{dish_id}")
def delete_dish(dish_id: int, session: Session = Depends(get_session), admin=Depends(get_current_admin)):
    result = service.delete_dish(session, dish_id)
    return result


@router.post("/{dish_id}/image")
def upload_dish_image(
    dish_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    admin=Depends(get_current_admin)
):
    
    image_url = upload_image(file.file)
    
    
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    
    dish.image_url = image_url
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return {"image_url": image_url}