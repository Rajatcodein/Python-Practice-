from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Mithai(BaseModel):
    id: int
    name : str
    origin : str

box: list[Mithai]=[]
@app.get("/")
def Read():
    return{" message ":" welcome to data engineeing world"} 
@app.get("/Sweet")
def get_Mithai():
    return Mithai
@app.post("/sugar")
def add_Mithai(Mithai:Mithai):
    box.append(Mithai)
    return Mithai
@app.put("/ Mithai/{Mithai_id}")
def update_tea(Mithai_id:int,updated_Mithai:Mithai):
    for index ,Mithai in enumerate(box):
        if Mithai.id ==Mithai_id:
            box[index]=updated_Mithai
            return updated_Mithai
        return{"erro": " sweets not found"}
@app.delete("/ Mithai/{Mithai_id}")
def del_tea(Mithai_id:int,updated_Mithai:Mithai):
    for index ,Mithai in enumerate(box):
        if Mithai.id ==Mithai_id:
            delete=box.pop(index)
            return delete
        return{"erro": " sweets not found"}


