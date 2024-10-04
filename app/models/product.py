from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Product(Base):
    """
    Represents a product in the database.

    Attributes:
    - id (int): The primary key of the product.
    - name (str): The name of the product.
    - description (str): The description of the product.
    - price (float): The price of the product.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)