from fastapi import FastAPI, Query
from ohlc_service import get_ohlcv

app = FastAPI()

@app.get("/ohlc")
def fetch_ohlc(symbol: str = Query(..., description="Stock ticker symbol, uppercase")):
    return get_ohlcv(symbol)
