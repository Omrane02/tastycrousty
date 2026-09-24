from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.modules.restaurants.models import Restaurant
from src.modules.restaurants.schemas import (
    RestaurantResponse,
    RestaurantUpdate,
    RestaurantAvailabilityUpdate,
)

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])



@router.get("", response_model=List[RestaurantResponse])
def get_all_restaurants(db: Session = Depends(get_db)):
    """Liste tous les restaurants de l'enseigne."""
    return db.query(Restaurant).all()



@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'un restaurant spécifique."""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant introuvable.",
        )
    return restaurant



@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant_in: RestaurantUpdate,
    db: Session = Depends(get_db),
    
):
    """Met à jour les informations d'un restaurant (heures, contact, adresse)."""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant introuvable.",
        )

    update_data = restaurant_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)
    return restaurant



@router.patch("/{restaurant_id}/availability", response_model=RestaurantResponse)
def update_restaurant_availability(
    restaurant_id: int,
    availability_in: RestaurantAvailabilityUpdate,
    db: Session = Depends(get_db),
   
):
    """Ouvre ou ferme un restaurant."""
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant introuvable.",
        )

    restaurant.is_open = availability_in.is_open
    db.commit()
    db.refresh(restaurant)
    return restaurant