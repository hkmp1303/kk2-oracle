import io
import logging
import pandas as pd
from logging import basicConfig, getLogger
from contextlib import asynccontextmanager
from app.chain.pipeline import Pipeline
from app.chain.steps import load_model, unload_model, model_loaded, model_name
from pandas.errors import EmptyDataError
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse as Json
from app.config import config
from app.data import Data
from app.schemas import AIReq, AIResp, Stats, Status, Upload
from typing import Any, AsyncGenerator

def listen() -> None:
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.host,
        port=config.port,
        reload=True
    )

@asynccontextmanager
async def load_ai(app: FastAPI) -> AsyncGenerator[None, Any, None]:
    load_model()
    yield
    unload_model()

def routes() -> FastAPI:
    app = FastAPI(
        title=config.app_name,
        description="Ask the oracle about your CSV-data",
        lifespan=load_ai
    )

    @app.get("/health", response_model=Status)
    async def health() -> Json:
        if not model_loaded:
            return Json(status_code=425, content={"status": "Too soon, AI model not loaded"})
        return Json(status_code=200, content={"status": "ok"})

    @app.post("/data/upload", response_model=Upload)
    async def upload(file: UploadFile = File(...)) -> Json:
        data = await file.read()
        try:
            Data(pd.read_csv(io.BytesIO(data)))
        except EmptyDataError as e:
            return Json(status_code=400, content={"status": "File is empty", "size": 0})
        except Exception as e:
            return Json(status_code=422, content={"status": "Could not read file: "+e, "size": 0})
        return Json(status_code=200, content={"status": "ok", "size": len(data)})

    @app.get("/data/stats", response_model=Stats)
    async def stats() -> Json:
        shape = Data.getShape()
        if shape is None:
            return Json(status_code=412, content={"status": "No data loaded"})
        return Json(status_code=200, content={
            "status": "ok",
            "rows": Data.getShape()[0],
            "cols": Data.getShape()[1],
            "desc": Data.desc()
        })

    @app.post("/ai/ask", response_model=AIResp)
    async def ask(body: AIReq) -> Json:
        print("q:"+body.q)
        if not model_loaded:
            return Json(status_code=425, content={"status": "Model not loaded", "m": model_name()})
        if Data.data is None:
            return Json(status_code=412, content={"status": "No data loaded", "m": model_name()})
        return Json(status_code=200, content={"status": "ok", "a": Pipeline.run(body.q), "m": model_name()})

    return app
basicConfig(level=logging.INFO)
app = routes()
