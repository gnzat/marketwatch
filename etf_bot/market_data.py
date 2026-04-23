import requests
from typing import Dict


def get_market_snapshot() -> Dict[str, object]:
    symbols = {
        "^GSPC": "sp500_change_pct",
        "^IXIC": "nasdaq_change_pct",
        "^DJI": "dow_change_pct",
    }
    snapshot = {}
    for symbol, key in symbols.items():
        try:
            response = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                params={"interval": "2m", "range": "1d"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            result = data["chart"]["result"][0]
            closes = result["indicators"]["adjclose"][0]["adjclose"]
            if closes and len(closes) >= 2:
                first, latest = closes[0], closes[-1]
                snapshot[key] = round((latest - first) / first * 100, 2)
            else:
                snapshot[key] = 0.0
        except Exception:
            snapshot[key] = 0.0

    if snapshot["sp500_change_pct"] < -0.2:
        risk_tone = "defensive"
    elif snapshot["sp500_change_pct"] > 0.4:
        risk_tone = "risk-on"
    else:
        risk_tone = "balanced"

    if snapshot["nasdaq_change_pct"] >= snapshot["sp500_change_pct"]:
        top_theme = "tech"
    elif snapshot["sp500_change_pct"] < 0:
        top_theme = "defensive"
    else:
        top_theme = "broad market"

    snapshot.update({"top_theme": top_theme, "risk_tone": risk_tone})
    return snapshot
import requests
from config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"

def get_quote(symbol: str) -> dict:
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(BASE_URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    quote = data.get("Global Quote", {})
    return {
        "symbol": symbol,
        "price": quote.get("05. price"),
        "change": quote.get("09. change"),
        "change_percent": quote.get("10. change percent"),
    }

#create market snapshot
def get_market_snapshot() -> dict:
    spy = get_quote("SPY")
    qqq = get_quote("QQQ")
    xlk = get_quote("XLK")
    xlv = get_quote("XLV")

    def pct_to_float(p):
        try:
            return float(str(p).replace("%", ""))
        except:
            return 0.0

    spy_pct = pct_to_float(spy["change_percent"])
    qqq_pct = pct_to_float(qqq["change_percent"])
    xlk_pct = pct_to_float(xlk["change_percent"])
    xlv_pct = pct_to_float(xlv["change_percent"])

    if qqq_pct > spy_pct and xlk_pct > 0:
        top_theme = "tech"
        risk_tone = "risk-on"
    elif xlv_pct > spy_pct:
        top_theme = "defensive"
        risk_tone = "defensive"
    else:
        top_theme = "broad"
        risk_tone = "neutral"

    return {
        "indices": {
            "SPY": spy,
            "QQQ": qqq,
            "XLK": xlk,
            "XLV": xlv,
        },
        "top_theme": top_theme,
        "risk_tone": risk_tone,
    }