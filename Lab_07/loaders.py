from __future__ import annotations
from functools import singledispatch
from pathlib import Path
import io
import json
import csv
from typing import List, Dict, Any

@singledispatch
def load_inventory(src: Any) -> List[Dict[str, Any]]:
    """Поліморфний завантажувач складських запасів."""
    raise TypeError(f"Unsupported source type: {type(src)!r}")

@load_inventory.register
def _(src: str) -> List[Dict[str, Any]]:
    s = src.strip()
    if not s:
        return []
    
    if s.startswith("[") or s.startswith("{"):
        data = json.loads(s)
        return data if isinstance(data, list) else [data]
    
    path_obj = Path(src)
    if path_obj.exists():
        content = path_obj.read_text(encoding="utf-8")
        if path_obj.suffix.lower() == ".csv":
            f = io.StringIO(content)
            reader = csv.DictReader(f)
            return list(reader)
        else:
            data = json.loads(content)
            return data if isinstance(data, list) else [data]
    
    if "," in s and "\n" in s:
        f = io.StringIO(s)
        reader = csv.DictReader(f)
        return list(reader)
        
    raise ValueError("Unrecognized string format for inventory data.")

@load_inventory.register
def _(src: Path) -> List[Dict[str, Any]]:
    content = src.read_text(encoding="utf-8")
    if src.suffix.lower() == ".csv":
        f = io.StringIO(content)
        reader = csv.DictReader(f)
        return list(reader)
    else:
        data = json.loads(content)
        return data if isinstance(data, list) else [data]

@load_inventory.register
def _(src: io.TextIOBase) -> List[Dict[str, Any]]:
    content = src.read()
    content_stripped = content.strip()
    if content_stripped.startswith("[") or content_stripped.startswith("{"):
        data = json.loads(content)
        return data if isinstance(data, list) else [data]
    else:
        f = io.StringIO(content)
        reader = csv.DictReader(f)
        return list(reader)

@load_inventory.register
def _(src: list) -> List[Dict[str, Any]]:
    if src and not isinstance(src[0], dict):
        raise ValueError("Expected list of dictionaries for inventory items.")
    return src