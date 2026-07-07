from pydantic import BaseModel

class Upload(BaseModel):
    status: str
    size: int

class Stats(BaseModel):
    status: str
    cols: int
    rows: int

class AIResp(BaseModel):
    a: str
    m: str
