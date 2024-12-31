import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Product:
    """
    A class that used to create new objects (products) to encapsulate product info (id, name, description, quantity, price)
    Also provide product specific methods (apply_discount, prod_in_stock)
    """
    def __init__(self, prod_id, prod_name, prod_description, prod_price, prod_quantity):
        self.id = prod_id # UID for the product
        self.name = prod_name # Name of the product
        self.description = prod_description # Description of the product
        self.price = prod_price # Price of the product
        self.quantity = prod_quantity # Quantity of the product

    def __str__(self):
        return f"{self.name} costs {self.price} dollars."
    
    def __repr__(self):
        return f"Product({self.id}, {self.name}, {self.price}, {self.quantity})"
    
    def apply_discount(self, prod_id, prod_name, prod_price, discount: float):
        discounted_price = prod_name * discount
        logger.info(f"Update Done for Prod_id: {prod_id}, \nProduct original price: {prod_price}\nProduct discounted price: {discounted_price}")

        return discounted_price
    