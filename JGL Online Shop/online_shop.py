"""Imports online_shop.db and allows queries"""

from sqlalchemy import create_engine, Column, DateTime, Float, Integer, String
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
    
class LeatherColors(Base):
    __tablename__ = "leather_colors"
    leather_color_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    hex_color = Column(String(200), unique=True, nullable=False) 
    color_string = Column(String(200), unique=True, nullable=False) 

class LeatherGoods(Base):
    __tablename__ = "leather_goods"
    leather_item_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    item = Column(String(200), unique=True, nullable=False)       
      
class MetalColors(Base):
    __tablename__ = "metal_colors"
    metal_color_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    metal_type = Column(String(200), unique=True, nullable=False)
    
class Sizes(Base):
    __tablename__ = "sizes"
    size_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    size_inches = Column(Integer, unique=True, nullable=False)
    size_centimeters = Column(Float, unique=True, nullable=False)
    
class WritingOptions(Base):
    __tablename__ = "writing_options"
    option_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    product_type = Column(String(200), unique=True, nullable=False)
