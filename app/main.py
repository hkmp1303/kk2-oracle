import io
import pandas as pd
from pandas.errors import EmptyDataError
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse as Json
from app.config import config
from app.data import Data
from app.schemas import AIResp, Stats, Upload

def listen():
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.host,
        port=config.port,
        reload=True
    )

def routes():
    app = FastAPI(
        title=__name__,
        description="Ask the oracle about your CSV-data",
    )

    @app.get("/")
    def root():
        return {"hello from root v" + app.version}

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/data/upload", response_model=Upload)
    async def upload(file: UploadFile = File(...)):
        data = await file.read()
        try:
            Data(pd.read_csv(io.BytesIO(data)))
        except EmptyDataError as e:
            return Json(status_code=400, content={"status": "File is empty", "size": 0})
        except Exception as e:
            return Json(status_code=422, content={"status": "Could not read file: "+e, "size": 0})
        return Json(status_code=200, content={"status": "ok", "size": len(data)})

    @app.get("/data/stats", response_model=Stats)
    def stats():
        shape = Data.getShape()
        if shape is None:
            return Json(status_code=412, content={"status": "No data loaded"})
        return Json(status_code=200, content={"status": Data.getShape()})

    @app.post("/ai/ask")
    def ask(q: str):
        pass

    return app

app = routes()
