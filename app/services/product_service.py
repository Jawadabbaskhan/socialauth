from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate):
    """
    Creates a new product in the database.

    Parameters:
    - db (Session): The database session.
    - product (ProductCreate): The product data to create.

    Returns:
    - Product: The created product.
    """
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    """
    Retrieves a product by its ID.

    Parameters:
    - db (Session): The database session.
    - product_id (int): The ID of the product to retrieve.

    Returns:
    - Product or None: The retrieved product or None if not found.
    """
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieves a list of products with pagination.

    Parameters:
    - db (Session): The database session.
    - skip (int): The number of products to skip.
    - limit (int): The maximum number of products to return.

    Returns:
    - list[Product]: A list of retrieved products.
    """
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product: ProductUpdate):
    """
    Updates an existing product by its ID.

    Parameters:
    - db (Session): The database session.
    - product_id (int): The ID of the product to update.
    - product (ProductUpdate): The updated product data.

    Returns:
    - Product or None: The updated product or None if not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    """
    Deletes an existing product by its ID.

    Parameters:
    - db (Session): The database session.
    - product_id (int): The ID of the product to delete.

    Returns:
    - Product or None: The deleted product or None if not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product