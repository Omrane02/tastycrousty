from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import require_admin
from src.modules.users import service
from src.modules.users.schema import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, current_user: dict = Depends(require_admin)) -> UserRead:
    try:
        row = service.create_user(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UserRead(**row)