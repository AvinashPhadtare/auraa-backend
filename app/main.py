from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import os 
from app.api.v1.routes.user import order as user_order
from app.api.v1.routes.admin import orders as admin_orders
from contextlib import asynccontextmanager
from app.models.order import Order
from app.models.order_item import OrderItem
from app.db.session import engine
from app.api.v1.routes import dish, auth
from app.api.v1.routes.public import menu
from app.api.v1.routes.admin import reports as admin_reports



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("static/qr", exist_ok=True)
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "https://b43cc890-auraa-management.phadtareavinash2008.workers.dev",
        "https://auraa-frontend-weld.vercel.app",
        "https://auraa-resto-management.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth.router,prefix="/admin", tags=["🎈 Admin - Auth"])
app.include_router(dish.router, prefix="/admin/dishes", tags=["🎈 Admin - Dishes"])
app.include_router(admin_orders.router, prefix="/admin/orders", tags=["🎈 Admin - Orders"])
app.include_router(admin_reports.router, prefix="/admin/reports", tags=["🎈 Admin - Reports"])
app.include_router(menu.router, tags=["✨✨ Customer DashBoard ✨✨"])
app.include_router(user_order.router, prefix="/user/order", tags=["✨ Customer - Orders"])
