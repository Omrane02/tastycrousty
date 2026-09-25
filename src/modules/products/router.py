from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import check_restaurant_access, get_current_user
from src.modules.products import service
from src.modules.products.schema import (
    ProductAvailabilityUpdate,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    category: str | None = None,
    q: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
) -> list[ProductRead]:
    rows = service.list_products(category, q, restaurant_id, is_available)

    if q is not None and not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucun produit trouvé avec '{q}'",
        )

    return [ProductRead(**row) for row in rows]

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int) -> ProductRead:
    row = service.get_product(product_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
    return ProductRead(**row)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    current_user: dict = Depends(get_current_user),
) -> ProductRead:
    check_restaurant_access(current_user, data.restaurant_id)
    try:
        row = service.create_product(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return ProductRead(**row)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user: dict = Depends(get_current_user),
) -> ProductRead:
    existing = service.get_product(product_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")

    check_restaurant_access(current_user, existing["restaurant_id"])

    row = service.update_product(product_id, data)
    return ProductRead(**row)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: dict = Depends(get_current_user),
) -> None:
    existing = service.get_product(product_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")

    check_restaurant_access(current_user, existing["restaurant_id"])
    service.delete_product(product_id)


@router.patch("/{product_id}/availability", response_model=ProductRead)
def update_availability(
    product_id: int,
    data: ProductAvailabilityUpdate,
    current_user: dict = Depends(get_current_user),
) -> ProductRead:
    existing = service.get_product(product_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")

    check_restaurant_access(current_user, existing["restaurant_id"])

    row = service.update_availability(product_id, data.is_available)
    return ProductRead(**row)