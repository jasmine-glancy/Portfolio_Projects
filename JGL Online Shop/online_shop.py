"""Imports online_shop.db and allows queries"""

from sqlalchemy import create_engine, Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Define database URI
ONLINE_SHOP_URI = "sqlite:///online_shop.db"

# Create engines for the database
shop_engine = create_engine(ONLINE_SHOP_URI)

# Create session for the database
ShopSession = sessionmaker(bind=shop_engine)
SHOP_SESSION = ShopSession()

class Base(DeclarativeBase):
    pass

# Define modules that map to the tables in the existing database
class ProductsAndServices(Base):
    __tablename__ = "products_and_services"
    service_product_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    rate_unit = Column(String(20), nullable=False)
    notes = Column(String(200))
    last_updated = Column(DateTime, nullable=False)
    image_path = Column(String(200))