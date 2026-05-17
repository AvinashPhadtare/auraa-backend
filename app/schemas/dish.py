from pydantic import BaseModel, Field, ConfigDict
from app.models.dish import DishCategory

class DishCreate(BaseModel):
    dish_name: str = Field(min_length=1)
    price: int = Field(ge=0)
    category: DishCategory = DishCategory.main_course

class DishUpdate(BaseModel):
    dish_name: str | None = None
    price: int | None = Field(default=None, ge=0)
    category: DishCategory | None = None

class DishResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    dish_name: str
    price: int
    category: str
    image_url: str | None = None
