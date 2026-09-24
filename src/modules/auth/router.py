from fastapi import APIRouter, HTTPException, status

from src.core.security import create_access_token
from src.modules.auth import service
from src.modules.auth.schema import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(data: LoginRequest) -> Token:
    user = service.authenticate_user(data.username, data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant ou mot de passe incorrect.",
        )

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user ["role"],
            "restaurant_id": user ["restaurant_id"],
        }
    )
    return Token(access_token=access_token)