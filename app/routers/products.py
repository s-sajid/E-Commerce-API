from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=['Products']
)


# Get all products
@router.get("/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    product = db.query(models.Product).filter(models.Product.description.contains(search)).limit(limit).offset(skip).all()

    return product


# Create new product
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_products(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_product = models.Product(owner_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# Get product by ID
@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")

    return product


# Delete product by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {id} does not exist")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action")

    product_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update product by ID
@router.put("/{id}", response_model=schemas.Product)
def update_product(id: int, updated_product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with id: {id} does not exist")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action")

    product_query.update(updated_product.dict(), synchronize_session=False)
    db.commit()

    return product_query.first()
