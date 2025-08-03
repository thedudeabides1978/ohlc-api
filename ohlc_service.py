# ohlc_service.py   – Stooq version, no Cloudflare, no API key
from datetime import date, timedelta
import pandas as pd
import requests
from io import StringIO

def last_year_ohlcv(symbol: str) -> dict:
    """
    Return one year of OHLCV (daily) ending today as
    { "YYYY-MM-DD": {"Open": ..., "High": ... , ...}, ... }
    """
    url   = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    text  = requests.get(url, timeout=(5, 15)).text        # tiny response
    df    = pd.read_csv(StringIO(text), parse_dates=["Date"])
    today = date.today()
    start = today - timedelta(days=365)
    df    = df[(df["Date"] >= pd.Timestamp(start)) & (df["Date"] <= pd.Timestamp(today))]
    df.set_index("Date", inplace=True)
    return df.to_dict(orient="index")
