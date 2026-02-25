# mithai_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Mithai(BaseModel):
    id: int
    name: str
    origin: str

box: List[Mithai] = []

@router.get("/")
def read_root():
    return {"message": "welcome to data engineering world"} 

@router.get("/sweets", response_model=List[Mithai])
def get_mithai():
    return box

@router.post("/sugar", response_model=Mithai)
def add_mithai(mithai: Mithai):
    box.append(mithai)
    return mithai

@router.put("/mithai/{mithai_id}", response_model=Mithai)
def update_mithai(mithai_id: int, updated_mithai: Mithai):
    for index, m in enumerate(box):
        if m.id == mithai_id:
            box[index] = updated_mithai
            return updated_mithai
    raise HTTPException(status_code=404, detail="Sweet not found")

@router.delete("/mithai/{mithai_id}", response_model=Mithai)
def del_mithai(mithai_id: int):
    for index, m in enumerate(box):
        if m.id == mithai_id:
            return box.pop(index)
    raise HTTPException(status_code=404, detail="Sweet not found")