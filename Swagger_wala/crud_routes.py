# crud_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Pydantic model (schema) for an item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory "DB"
items_db: List[Item] = []

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    items_db.append(item)
    return item

@router.get("/items/", response_model=List[Item])
def read_items():
    return items_db

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[idx]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")