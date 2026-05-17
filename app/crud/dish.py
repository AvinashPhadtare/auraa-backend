from sqlmodel import Session,select
from app.models.dish import Dish
from app.schemas.dish import DishCreate,DishUpdate

def get_dish_by_name(session:Session, dish_name: str):
    existing_result = session.exec(
        select(Dish).where(Dish.dish_name.ilike(dish_name))
    ).first()
    return existing_result

def get_dish_by_id(session: Session, dish_id: int):
    dish = session.get(Dish, dish_id)
    return dish

def get_all_dishes(session: Session):
    result = session.exec(select(Dish)).all()
    return result

def create_dish(session: Session, dish_data: DishCreate):
    dish = Dish(dish_name=dish_data.dish_name, price=dish_data.price, category=dish_data.category) 
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish

def update_dish(session: Session,dish: Dish,new_data: DishUpdate):
    if new_data.dish_name is not None:
        dish.dish_name = new_data.dish_name
    if new_data.price is not None:
        dish.price = new_data.price
    if new_data.category is not None:
        dish.category = new_data.category
    session.commit()
    session.refresh(dish)

    return dish

def delete_dish(session: Session, dish: Dish):
    session.delete(dish)
    session.commit()