from typing import Tuple
import pandas as pd

class Data:
    # pandas object
    data: pd.DataFrame | None = None

    def __init__(_, df: pd.DataFrame):
        Data.data = df

    def getShape() -> Tuple[int, int] | None:
        if Data.data is None:
            return None
        return Data.data.shape

    def desc() -> dict:
        return Data.data.describe().to_dict(orient="index")
