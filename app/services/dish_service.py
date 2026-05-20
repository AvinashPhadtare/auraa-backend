from sqlmodel import Session
from fastapi import HTTPException, UploadFile
from app.crud import dish as crud
from app.schemas.dish import DishCreate, DishUpdate, DishResponse 
from app.utils.cloudinary import upload_image 

def add_dish(session:Session, dish_data: DishCreate):
    dish = crud.get_dish_by_name(session, dish_data.dish_name)

    if dish:
        raise HTTPException(status_code=400, detail="Dish already exists")
    
    new_dish = crud.create_dish(session, dish_data)
    return DishResponse.model_validate(new_dish)

def get_all_dishes(session):
    dishes = crud.get_all_dishes(session)
    return [DishResponse.model_validate(d) for d in dishes]

def update_dish(session:Session, dish_id, new_data: DishUpdate):
    dish_by_id = crud.get_dish_by_id(session, dish_id)

    if not dish_by_id:
        raise HTTPException(status_code=404, detail="Dish not Found")

    if new_data.dish_name is None and new_data.price is None and new_data.category is None:
        raise HTTPException(status_code=400, detail="Nothing to update")
    
    if new_data.dish_name is not None:
        existing = crud.get_dish_by_name(session, new_data.dish_name)
        if existing and existing.id != dish_id:
            raise HTTPException(status_code=400, detail="Dish with this name already exists")
    
    updated_dish = crud.update_dish(session, dish_by_id, new_data)

    return DishResponse.model_validate(updated_dish)

def delete_dish(session:Session, dish_id):
    dish = crud.get_dish_by_id(session, dish_id)

    if not dish:
        raise HTTPException(status_code=404, detail="Dish not Found")
    
    crud.delete_dish(session, dish)

    return {"message": "Dish deleted successfully"}



def upload_dish_image(session, dish_id: int, file: UploadFile):
    dish = crud.get_dish_by_id(session, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    image_url = upload_image(file.file)

    dish.image_url = image_url
    session.commit()
    session.refresh(dish)

    return DishResponse.model_validate(dish)