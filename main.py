from fastapi import FastAPI, HTTPException, Query
from ohlc_service import last_year_ohlcv

app = FastAPI(title="OHLC micro-API")

@app.get("/ohlc")
def get_ohlc(symbol: str = Query(..., description="Ticker e.g. AAPL")):
    try:
        return last_year_ohlcv(symbol.upper())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
