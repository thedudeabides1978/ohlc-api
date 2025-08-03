from datetime import date, timedelta
import pandas as pd
import requests
from io import StringIO

def get_ohlcv(symbol: str) -> dict:
    url = f"https://stooq.com/q/d/l/?s={symbol.lower()}.us&i=d"
    text = requests.get(url, timeout=(5, 15)).text
    df = pd.read_csv(StringIO(text), parse_dates=["Date"])

    today = date.today()
    one_year_ago = today - timedelta(days=365)
    df = df[(df["Date"] >= pd.Timestamp(one_year_ago)) & (df["Date"] <= pd.Timestamp(today))]

    df = df.rename(columns={"Date": "date"})
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Ensure the dataframe only has the required columns, and correct order
    df = df[["date", "Open", "High", "Low", "Close", "Volume"]]

    return {
        "symbol": symbol.upper(),
        "data": df.to_dict(orient="records")
    }
