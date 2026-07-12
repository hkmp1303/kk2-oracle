from pydantic import BaseModel

class Upload(BaseModel):
    status: str
    size: int

class Stats(BaseModel):
    status: str
    cols: int
    rows: int
    desc: dict

class AIResp(BaseModel):
    a: str
    m: str
