from pydantic import BaseModel

class TotalBirths(BaseModel):
    year: int
    total_births: int
