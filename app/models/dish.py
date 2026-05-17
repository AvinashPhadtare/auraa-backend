from sqlmodel import SQLModel, Field
from enum import Enum

class DishCategory(str, Enum):
    starters = "Starters"
    main_course = "Main Course"
    desserts = "Desserts"
    drinks = "Drinks"
    specials = "Specials"


class Dish(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dish_name: str = Field(index=True, min_length=1)
    price: int = Field(ge=0)   
    category: DishCategory = DishCategory.main_course
    image_url: str | None = Field(default=None)

    