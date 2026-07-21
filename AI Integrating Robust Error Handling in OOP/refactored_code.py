class InvalidProductDataError(Exception):
    """Custom exception raised when product attributes fail validation rules."""
    pass


class Product:
    def __init__(self, name: str, price: float | int, quantity: int):
        self.name = name
        # Assigning through properties so validation runs during initialization as well
        self.price = price
        self.quantity = quantity

    # --- Price Property ---
    @property
    def price(self) -> float | int:
        return self._price

    @price.setter
    def price(self, value: float | int) -> None:
        # Note: bool is a subclass of int in Python, so we explicitly check `not isinstance(value, bool)`
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Invalid price: '{value}'. Price must be a numeric type (int or float)."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid price: {value}. Price cannot be negative."
            )
        self._price = value

    # --- Quantity Property ---
    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Invalid quantity: '{value}'. Quantity must be a numeric type."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid quantity: {value}. Quantity cannot be negative."
            )
        self._quantity = int(value)

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class InventoryManager:
    def __init__(self):
        self.inventory: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self.inventory[product.name] = product
        print(f"Added: {product}")

    def update_stock(self, name: str, new_quantity: int) -> None:
        if name in self.inventory:
            self.inventory[name].quantity = new_quantity
            print(f"Updated {name} quantity to {new_quantity}")
        else:
            print(f"Product '{name}' not found.")


# --- Demo Usage ---
if __name__ == "__main__":
    print("--- Normal Operations ---")
    try:
        p1 = Product("Laptop", 999.99, 10)
        manager = InventoryManager()
        manager.add_product(p1)
        manager.update_stock("Laptop", 15)
    except InvalidProductDataError as e:
        print(f"Validation Error: {e}")

    print("\n--- Validation Tests ---")

    # Test 1: Negative Price on Creation
    try:
        p2 = Product("Phone", -150.00, 5)
    except InvalidProductDataError as e:
        print(f"Caught expected error -> {e}")

    # Test 2: Passing a Boolean for Quantity
    try:
        p1.quantity = True  # In Python, True is an instance of int (True == 1)
    except InvalidProductDataError as e:
        print(f"Caught expected error -> {e}")

    # Test 3: Updating to a negative quantity
    try:
        manager.update_stock("Laptop", -5)
    except InvalidProductDataError as e:
        print(f"Caught expected error -> {e}")
