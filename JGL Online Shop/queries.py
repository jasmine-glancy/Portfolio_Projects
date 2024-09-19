"""In charge of querying the database"""

import online_shop as sh
# Create charge report session for queries
shop_session = sh.SHOP_SESSION

def find_product_list():
    """Returns a list of available product/service list"""
    
    products_and_services = shop_session.query(
        sh.ProductsAndServices
    ).all()
    
    print(products_and_services)
    
    return products_and_services

def find_product_by_id(product_id):
    """Queries a database for a product using its ID"""
    
    product_or_service = shop_session.query(
        sh.ProductsAndServices
    ).filter_by(service_product_id=product_id).first()
    
    return product_or_service

def find_leather_goods():
    """Returns a list of leather goods"""
    
    leather_goods = shop_session.query(
        sh.LeatherGoods
    ).all()
    
    return leather_goods

def look_up_leather_colors():
    """Returns a list of leather colors"""
    
    leather_colors = shop_session.query(
        sh.LeatherColors
    ).all()
    
    return leather_colors

def find_sizes():
    """Returns a list of sizes of leather products"""
    
    sizes = shop_session.query(
        sh.Sizes
    ).all()
    
    return sizes