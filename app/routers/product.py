from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB
from app.services.product_service import create_product, get_product, get_products, update_product, delete_product
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ProductInDB)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Logs out the user by deleting authentication cookies.

    Returns:
    - JSONResponse: A response indicating successful logout.
    """
    return create_product(db, product)


@router.get("/{product_id}", response_model=ProductInDB)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a list of products with pagination.

    Parameters:
    - skip (int): The number of products to skip.
    - limit (int): The maximum number of products to return.
    - db (Session): The database session dependency.

    Returns:
    - list[ProductInDB]: A list of retrieved products.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.get("/", response_model=list[ProductInDB])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip, limit)


@router.put("/{product_id}", response_model=ProductInDB)
def update_existing_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing product by its ID.

    Parameters:
    - product_id (int): The ID of the product to update.
    - product (ProductUpdate): The updated product data.
    - db (Session): The database session dependency.

    Returns:
    - ProductInDB: The updated product.
    """
    return update_product(db, product_id, product)


@router.delete("/{product_id}", response_model=ProductInDB)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    """
    Deletes an existing product by its ID.

    Parameters:
    - product_id (int): The ID of the product to delete.
    - db (Session): The database session dependency.

    Returns:
    - ProductInDB: The deleted product.
    """
    return delete_product(db, product_id)