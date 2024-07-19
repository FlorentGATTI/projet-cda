from pydantic import BaseModel

class Prenom(BaseModel):
    name: str
    count: int
    year: int
    sex: str
    total_births: int
    proportion: float
