from __future__ import annotations
from functools import reduce, partial
from operator import itemgetter, methodcaller
from typing import Callable, Iterable, Any, List, Dict

from models import StockItem
from loaders import load_inventory

def pipeline(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Послідовне застосування функцій через reduce (конвеєр)."""
    return reduce(lambda acc, f: f(acc), funcs, value)

def mapf(fn: Callable[[Any], Any]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """Часткове застосування map для конвеєрів."""
    return partial(map, fn)

def filt(pred: Callable[[Any], bool]) -> Callable[[Iterable[Any]], Iterable[Any]]:
    """Часткове застосування filter для конвеєрів."""
    return partial(filter, pred)

def normalize_raw_item(row: Dict[str, Any]) -> Dict[str, Any]:
    """Нормалізує словник за допомогою operator."""
    get_sku = itemgetter("sku")
    get_name = itemgetter("name")
    get_cat = itemgetter("category")
    get_qty = itemgetter("qty")
    get_price = itemgetter("price")

    strip = methodcaller("strip")
    title = methodcaller("title")

    return {
        "sku": strip(str(get_sku(row))),
        "name": title(strip(str(get_name(row)))),
        "category": title(strip(str(get_cat(row)))),
        "qty": int(get_qty(row)),
        "price": float(get_price(row))
    }

def item_to_object(d: Dict[str, Any]) -> StockItem:
    return StockItem(**d)

def top_n(n: int) -> Callable[[List[Any]], List[Any]]:
    """Повертає лямбду для зрізу перших n елементів."""
    return lambda it: list(it)[:n]

def clean_and_rank_inventory(src: Any, min_qty: int = 1, top: int = 3) -> List[StockItem]:
    """
    Головна функція для варіанту 11. 
    Будує та виконує конвеєр обробки складських запасів.
    """
    is_available = lambda item: item.qty >= min_qty

    result = pipeline(
        src,
        load_inventory,            
        mapf(normalize_raw_item),   
        mapf(item_to_object),    
        filt(is_available),         
        list,                       
        partial(sorted, key=lambda s: (s.inventory_value, s.qty, s.sku), reverse=True),
        top_n(top)               
    )
    return result