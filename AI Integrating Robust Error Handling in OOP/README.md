# AI: Integrating Robust Error Handling in OOP

## Objective
Apply AI-driven scaffolding (Gemini Code Assist) to enhance the `Product` class from the
Refactored Object-Oriented Product Inventory Manager with robust data validation and
custom exception handling, using Python's `@property` decorator.

## AI Tool Used
Gemini Code Assist (VS Code sidebar)

## Files in This Folder
| File | Description |
|---|---|
| `initial_code.py` | The starting, unvalidated `Product` / `InventoryManager` code provided in the task. |
| `refactored_code.py` | The AI-scaffolded version returned by Gemini Code Assist: `price` and `quantity` are now `@property`-based with setter validation, backed by a custom `InvalidProductDataError` exception, plus type hints, a `__repr__`, and a dictionary-based inventory. |
| `screenshot.png` | Screenshot of the prompt and Gemini Code Assist's full response (code + explanation). |

## What Changed
- Added a custom exception class, `InvalidProductDataError(Exception)`.
- Converted `price` and `quantity` into properties (`@property` / `@x.setter`) on `Product`.
- Each setter rejects non-numeric types (including `bool`, since `bool` is a subclass of
  `int` in Python) and negative values, raising `InvalidProductDataError` with a descriptive
  message instead of letting the object reach an invalid state.
- `InventoryManager` was reshaped to use a `name -> Product` dictionary (`self.inventory`)
  and an `update_stock()` method; both `add_product()` and `update_stock()` benefit
  automatically from validation because they assign through `product.quantity`.
- Added a `__repr__` for readable printing, and a demo block with three validation tests:
  a negative price at construction, a boolean assigned to quantity, and a negative
  quantity update.

## Why This Matters (Data Integrity & Encapsulation)
Because `price` and `quantity` are properties, every assignment to them — at construction,
through `update_stock()`, or from any future code — is routed through the same validation
logic. There is no way to bypass the check without deliberately touching the private
`_price` / `_quantity` attributes. Using a dedicated `InvalidProductDataError` (rather than
a generic exception or no handling at all) lets calling code catch and respond to "bad
product data" specifically — logging it or messaging a user — while the rest of the
application keeps running instead of crashing.
