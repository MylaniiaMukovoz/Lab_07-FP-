from __future__ import annotations
from core import clean_and_rank_inventory
from models import StockItem

def main() -> None:
    print("ДЕМОНСТРАЦІЯ ЛАБОРАТОРНОЇ РОБОТИ №7 (Варіант 11: Складські запаси)")

    raw_json = (
        '[{"sku": "A-01", "name": "  laptop   ", "category": " electronics ", "qty": "5", "price": "1200.0"},'
        '{"sku": "A-02", "name": "mouse", "category": "electronics", "qty": "0", "price": "25.5"},'
        '{"sku": "B-01", "name": "office desk", "category": "furniture", "qty": "10", "price": "300.0"},'
        '{"sku": "C-01", "name": "ergonomic chair", "category": "furniture", "qty": "4", "price": "250.0"},'
        '{"sku": "A-03", "name": "usb-c cable", "category": "accessories", "qty": "50", "price": "15.0"}]'
    )

    print("\n1. Завантаження та ранжування складських запасів (Top 3 з qty >= 1):")
    top_items = clean_and_rank_inventory(raw_json, min_qty=1, top=3)
    for idx, item in enumerate(top_items, 1):
        print(f"  {idx}. {item} | Загальна вартість: {item.inventory_value}")

    print("\n2. Перевірка total_ordering та порівняння об'єктів:")
    item1 = StockItem("A-01", "Laptop", "Electronics", 5, 1200.0) 
    item2 = StockItem("B-01", "Desk", "Furniture", 10, 300.0)   
    print(f"  {item1} > {item2} -> {item1 > item2}")
    print(f"  {item1} <= {item2} -> {item1 <= item2}")

    print("\nДемонстрація успішно завершена!")

if __name__ == "__main__":
    main()