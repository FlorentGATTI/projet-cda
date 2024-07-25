from pydantic import BaseModel

class NameData(BaseModel):
    name: str
    count: int
