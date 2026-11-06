from __future__ import annotations
import pytest
from pathlib import Path
import io
from functools import reduce
from operator import mul

from models import StockItem
from loaders import load_inventory
from core import pipeline, clean_and_rank_inventory

def test_reduce_basic():
    """Тестування базового застосування reduce."""
    assert reduce(mul, [1, 2, 3, 4], 1) == 24
    assert reduce(mul, [], 1) == 1

def test_pipeline():
    """Тестування правильності виконання конвеєра (pipeline)."""
    inc = lambda x: x + 1
    dbl = lambda x: x * 2
    assert pipeline(3, inc, dbl, inc) == 9  

def test_total_ordering():
    """Тестування об'єктів @total_ordering."""
    s1 = StockItem("A-01", "Laptop", "Electronics", 5, 1200.0)
    s2 = StockItem("B-01", "Desk", "Furniture", 10, 300.0)      
    s3 = StockItem("A-02", "Mouse", "Electronics", 5, 1200.0)   

    assert s1 > s2
    assert s2 < s1
    assert s1 <= s3  
    assert s1 == StockItem("A-01", "Laptop", "Electronics", 5, 1200.0)
    with pytest.raises(TypeError):
        _ = s1 > "not a stock item"

def test_singledispatch_loaders(tmp_path):
    """Тестування поліморфного завантажувача з різними типами входів."""
    json_str = '[{"sku": "X-1", "name": "Item 1", "category": "Cat", "qty": 2, "price": 10.0}]'
    
    res1 = load_inventory(json_str)
    assert len(res1) == 1
    assert res1[0]["sku"] == "X-1"

    p_json = tmp_path / "test.json"
    p_json.write_text(json_str, encoding="utf-8")
    res2 = load_inventory(p_json)
    assert res2[0]["name"] == "Item 1"

    csv_str = "sku,name,category,qty,price\nY-1,Mouse,Accessory,5,20.0"
    p_csv = tmp_path / "test.csv"
    p_csv.write_text(csv_str, encoding="utf-8")
    res3 = load_inventory(p_csv)
    assert len(res3) == 1
    assert res3[0]["sku"] == "Y-1"

    f_io = io.StringIO(json_str)
    res4 = load_inventory(f_io)
    assert len(res4) == 1

    res5 = load_inventory(res1)
    assert res5 == res1

    with pytest.raises(TypeError):
        load_inventory(12345)

def test_clean_and_rank_inventory():
    """Тестування головного конвеєра обробки складських запасів."""
    data = [
        {"sku": "S-1", "name": "item a", "category": "cat1", "qty": 2, "price": 100.0},
        {"sku": "S-2", "name": "item b", "category": "cat1", "qty": 5, "price": 100.0},
        {"sku": "S-3", "name": "item c", "category": "cat2", "qty": 0, "price": 50.0} 
    ]
    top = clean_and_rank_inventory(data, min_qty=1, top=2)
    assert len(top) == 2
    assert top[0].sku == "S-2"
    assert top[1].sku == "S-1"