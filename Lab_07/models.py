from __future__ import annotations
from functools import total_ordering
from typing import Any

@total_ordering
class StockItem:
    """Клас для зберігання даних про складський запас."""
    
    def __init__(self, sku: str, name: str, category: str, qty: int, price: float) -> None:
        self.sku = str(sku).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.qty = int(qty)
        self.price = float(price)

    @property
    def inventory_value(self) -> float:
        """Загальна вартість позиції на складі."""
        return self.qty * self.price

    def __repr__(self) -> str:
        return (f"StockItem(sku={self.sku!r}, name={self.name!r}, "
                f"category={self.category!r}, qty={self.qty}, price={self.price})")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StockItem):
            return NotImplemented
        return (self.inventory_value, self.qty, self.sku) == (other.inventory_value, other.qty, other.sku)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, StockItem):
            return NotImplemented
        return (self.inventory_value, self.qty, self.sku) < (other.inventory_value, other.qty, other.sku)