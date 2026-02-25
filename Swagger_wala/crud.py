from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic model (schema) for an item
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory "DB"
items_db: List[Item] = []

# Create
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items_db.append(item)
    return item

# Read all
@app.get("/items/", response_model=List[Item])
def read_items():
    return items_db

# Read one
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Update
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[idx]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")