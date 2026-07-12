from pydantic import BaseModel
from typing import Optional

#region Pipeline schemas

class GeneratedPrompt(BaseModel):
    prompt: str

class GenPrompt(BaseModel):
    prefix_prompt: str = "Check yourself before you wreck yourself"
    q: str

class LLMOutput(BaseModel):
    response: list[dict[str, str]]

#endregion

#region FastAPI schemas

class AIReq(BaseModel):
    q: str

class AIResp(BaseModel):
    status: str
    a: Optional[str] = None
    m: str

class Stats(BaseModel):
    status: str
    cols: int
    rows: int
    desc: dict

class Status(BaseModel):
    status: str

class Upload(BaseModel):
    status: str
    size: int

#endregion
