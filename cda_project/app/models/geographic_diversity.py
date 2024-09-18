from pydantic import BaseModel
from typing import Optional

class NameDataByState(BaseModel):
    State: str
    Year: int
    Sex: str
    Name: str
    Count: int

class NameDataByTerritory(BaseModel):
    Territory: str
    Year: int
    Sex: str
    Name: str
    Count: int
