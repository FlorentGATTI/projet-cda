from pydantic import BaseModel
from typing import Optional

class NameDataByState(BaseModel):
    State: str
    Sex: str
    Year: int
    Name: str
    Count: int

class NameDataByTerritory(BaseModel):
    Territory: str
    Sex: str
    Year: int
    Name: str
    Count: int
