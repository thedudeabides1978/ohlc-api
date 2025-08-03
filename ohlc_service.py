from datetime import date, timedelta
import pandas as pd
import requests
from io import StringIO

def last_year_ohlcv(symbol: str) -> list:
    url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    text = requests.get(url, timeout=(5, 15)).text
    df = pd.read_csv(StringIO(text), parse_dates=["Date"])
    
    today = date.today()
    one_year_ago = today - timedelta(days=365)
    df = df[(df["Date"] >= pd.Timestamp(one_year_ago)) & (df["Date"] <= pd.Timestamp(today))]
    
    df = df.rename(columns={"Date": "date"})
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    
    return df.to_dict(orient="records")
