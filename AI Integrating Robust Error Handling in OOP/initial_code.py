# Refactored Object-Oriented Product Inventory Manager (Starting Point for Task)

class Product:
    """Represents a product with a name, price, and quantity."""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class InventoryManager:
    """Manages the collection of products and provides inventory operations."""
    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        """Adds a product object to the inventory list."""
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        """Updates the quantity of a product by name."""
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self):
        """Calculates the total monetary value of all inventory."""
        total = 0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x {product.quantity}")

# Demo Usage
manager = InventoryManager()
manager.add_product(Product("Laptop", 1200.00, 5))
manager.add_product(Product("Mouse", 25.00, 20))
manager.update_quantity("Mouse", 18)

print("Current Inventory:")
manager.display_inventory()
print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}")
