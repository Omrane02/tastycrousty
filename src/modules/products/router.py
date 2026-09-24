from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session


from src.modules.products.models import Product
from src.modules.products.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductAvailabilityUpdate,
)

router = APIRouter(prefix="/products", tags=["Products"])



@router.get("", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    q: Optional[str] = Query(None, description="Recherche textuelle dans le nom/description"),
    restaurant_id: Optional[int] = Query(None, description="Filtrer par id de restaurant"),
    is_available: Optional[bool] = Query(None, description="Filtrer par disponibilité"),
    db: Session = Depends(get_db),
):
    """
    Récupère la liste des produits avec filtres optionnels combinables.
    """
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if q:
        query = query.filter(
            (Product.name.ilike(f"%{q}%")) | (Product.description.ilike(f"%{q}%"))
        )
    if restaurant_id is not None:
        query = query.filter(Product.restaurant_id == restaurant_id)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    return query.all()



@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Récupère un produit par son ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable.",
        )
    return product



@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),

):
    """Ajoute un nouveau produit au catalogue."""
    new_product = Product(**product_in.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
   
):
    """Met à jour les informations d'un produit."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable.",
        )

    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product



@router.patch("/{product_id}/availability", response_model=ProductResponse)
def update_product_availability(
    product_id: int,
    availability_in: ProductAvailabilityUpdate,
    db: Session = Depends(get_db),
    
):
    """Active ou désactive la disponibilité d'un produit."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable.",
        )

    product.is_available = availability_in.is_available
    db.commit()
    db.refresh(product)
    return product



@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    
):
    """Supprime un produit du catalogue."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produit introuvable.",
        )

    db.delete(product)
    db.commit()
    return None