from pydantic import BaseModel
from typing import Optional

#region Pipeline schemas

class GeneratedPrompt(BaseModel):
    #system_prompt: str
    #user_prompt: str
    #dataset_batch: str
    prompt: str

class GenPrompt(BaseModel):
    prefix_prompt: str = "You are a helpful data analyst."
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
