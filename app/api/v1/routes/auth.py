from fastapi import APIRouter, HTTPException
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.schemas.auth import LoginRequest,TokenResponse

router = APIRouter()


@router.post("/login")
def login(data: LoginRequest):

    if data.username != settings.ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid Username")

    if not verify_password(data.password, settings.ADMIN_PASSWORD):
        raise HTTPException(status_code=401, detail="Invalid Password")

    token = create_access_token({"sub": settings.ADMIN_USERNAME})

    return TokenResponse(access_token=token)