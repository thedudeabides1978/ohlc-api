from datetime import date, timedelta
import requests, pandas as pd

def last_year_ohlcv(symbol: str):
    today = date.today()
    start = today - timedelta(days=365)

    url = f"https://api.nasdaq.com/api/quote/{symbol}/historical"
    hdrs = {"User-Agent": ("Mozilla/5.0 ... Chrome/125 Safari/537.36"),
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.nasdaq.com"}
    params = {"assetclass":"stocks","fromdate":start,"todate":today,"limit":9999}

    rows = requests.get(url, headers=hdrs, params=params, timeout=5, 30).json()\
                    ["data"]["tradesTable"]["rows"]

    df = (pd.DataFrame(rows)
            .rename(columns=str.title)               # Open → Open
            .assign(Date=pd.to_datetime(lambda x: x["Date"]))
            .set_index("Date")
            .apply(lambda c: pd.to_numeric(c.str.replace(",",""),
                                           errors="coerce"))
            .sort_index())
    return df.to_dict(orient="index")
