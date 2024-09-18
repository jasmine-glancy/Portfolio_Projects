"""In charge of querying the database"""

from online_shop import ProductsAndServices, SHOP_SESSION

# Create charge report session for queries
shop_session = SHOP_SESSION

def find_product_list():
    """Returns a list of available product/service list"""
    
    products_and_services = shop_session.query(
        ProductsAndServices
    ).all()
    
    print(products_and_services)
    
    return products_and_services

def find_product_by_id(product_id):
    """Queries a database for a product using its ID"""
    
    product_or_service = shop_session.query(
        ProductsAndServices
    ).filter_by(service_product_id=product_id).first()
    
    return product_or_service