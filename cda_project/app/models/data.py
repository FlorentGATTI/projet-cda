from pydantic import BaseModel
from typing import Dict

class TotalBirths(BaseModel):
    year: int
    total_births: int
    births_by_sex: Dict[str, int]
