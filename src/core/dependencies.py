from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from src.core.security import decode_access_token

security_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        ) -> dict:
            try:
                payload = decode_access_token(credentials.credentials)
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is invalid",
                )
            return {
            "username": payload.get("sub"),
            "role": payload.get("role"),
            "restaurant_id": payload.get("restaurant_id"),
        }
def require_admin( current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reserve a l'admin",)
    return current_user

def check_restaurant_access(current_user: dict, restaurant_id: int) -> None:
    if current_user["role"] == "admin":
        return
    if current_user["role"] == "staff" and current_user["restaurant_id"] == restaurant_id:
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Non autorisé a agir sur ce restaurant",
    )
