"""Imports online_shop.db and allows queries"""

from sqlalchemy import create_engine, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


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
class CartItems(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    session_id = Column(Integer, ForeignKey("shopping_sessions.session_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products_and_services.service_product_id"), nullable=False)
    quantity = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    leather_good_id = Column(Integer, ForeignKey("leather_goods.leather_item_id"))
    leather_color_id = Column(Integer, ForeignKey("leather_colors.leather_color_id"))
    metal_color_id = Column(Integer, ForeignKey("metal_colors.metal_color_id"))
    leather_goods_size_id = Column(Integer, ForeignKey("sizes.size_id"))
    writing_option_id = Column(Integer, ForeignKey("writing_options.option_id"))
    software_id = Column(Integer, ForeignKey("software_options.option_id"))
    
    # Define the relationship to ProductsAndServices
    product = relationship("ProductsAndServices", back_populates="cart_items")
    session = relationship("ShoppingSessions", back_populates="cart_items")

class Discounts(Base):
    __tablename__ = "discounts"
    discount_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(200), nullable=False)
    code = Column(String(15), unique=True)
    notes = Column(String(200))
    discount_percent = Column(Float)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
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
    
    # Define the relationships
    cart_items = relationship("CartItems", back_populates="product")
    order_items = relationship("OrderItems", back_populates="product")

    
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
    
class OrderDetails(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total = Column(Float)
    payment_id = Column(Integer, ForeignKey("payment_details.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
    # Define the relationships
    user = relationship("Users", back_populates="order_details")
    payment = relationship("PaymentDetails", back_populates="order_details")
    order_items = relationship("OrderItems", back_populates="order")

class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    order_id = Column(Integer, ForeignKey("order_details.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products_and_services.service_product_id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
    # Define the relationships
    order = relationship("OrderDetails", back_populates="order_items")
    product = relationship("ProductsAndServices", back_populates="order_items")

class PaymentDetails(Base):
    __tablename__ = "payment_details"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    amount = Column(Float, nullable=False)
    provider = Column(String(200), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
    # Define the relationships
    order_details = relationship("OrderDetails", back_populates="payment")

class ShoppingSessions(Base):
    __tablename__ = "shopping_sessions"
    session_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
    # Define the relationship
    user = relationship("Users", back_populates="shopping_sessions")
    cart_items = relationship("CartItems", back_populates="session")
    
class Sizes(Base):
    __tablename__ = "sizes"
    size_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    size_inches = Column(Integer, unique=True, nullable=False)
    size_centimeters = Column(Float, unique=True, nullable=False)
    
class SoftwareOptions(Base):
    __tablename__ = "software_options"
    option_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    product_type = Column(String(200), unique=True, nullable=False)

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(200), unique=True, nullable=False)
    password = Column(String(50), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    first_name = Column(String(200), unique=True)
    last_name = Column(String(200), unique=True)
    address = Column(String(500), unique=True)
    phone_number = Column(String(50), unique=True)
    created_at = Column(DateTime, nullable=False)
    modified_at = Column(DateTime, nullable=False)
    
    # Define the relationships
    shopping_sessions = relationship("ShoppingSessions", back_populates="user")
    order_details = relationship("OrderDetails", back_populates="user")
    
class WritingOptions(Base):
    __tablename__ = "writing_options"
    option_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    product_type = Column(String(200), unique=True, nullable=False)

