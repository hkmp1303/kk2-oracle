import io
import pandas as pd
from typing import Tuple

class Data:
    # pandas object
    data: pd.DataFrame | None = None

    def __init__(_, df: pd.DataFrame):
        Data.data = df

    @classmethod
    def clear(cls) -> None:
        cls.data = None

    @classmethod
    def getShape(cls) -> Tuple[int, int] | None:
        if cls.data is None:
            return None
        return cls.data.shape

    @classmethod
    def desc(cls) -> dict:
        return cls.data.describe().to_dict(orient="index")

    @classmethod
    def to_csv(cls, chunk_size: int = 20_000_000, csv_kwargs = None):
        return cls.data.to_csv()
        csv_kwargs = csv_kwargs or {} # create empty dict if not set

        buf = io.StringIO()
        cls.data.to_csv(buf, index=False, **csv_kwargs)
        text = buf.getvalue()
        lines = text.splitlines()
        header = lines[0]
        body = lines[1:]
        chunks = []
        curr = []
        curr_bytes = 0

        def flush():
            nonlocal curr, curr_bytes
            if not curr: return
            out = header + "\n" + "\n".join(curr) + "\n"
            chunks.append(out)
            curr, curr_bytes = [], 0

        for line in body:
            b = (line + "\n").encode("utf-8")
            if curr and curr_bytes + len(b) > chunk_size:
                flush()
            curr.append(line)
            curr_bytes += len(b)
        flush()
        return chunks
