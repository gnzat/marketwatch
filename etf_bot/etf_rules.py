# prevent gemini from inventing ETF symbols
ETF_LIBRARY = {
    "broad": [
        {"ticker": "VOO", "label": "Broad S&P 500 exposure"},
        {"ticker": "QQQ", "label": "Large-cap growth / Nasdaq exposure"},
    ],
    "tech": [
        {"ticker": "XLK", "label": "Technology sector exposure"},
        {"ticker": "QQQ", "label": "Growth and tech-heavy exposure"},
        {"ticker": "SOXX", "label": "Semiconductor exposure"},
    ],
    "defensive": [
        {"ticker": "XLV", "label": "Healthcare defensive exposure"},
        {"ticker": "XLP", "label": "Consumer staples defensive exposure"},
    ],
    "energy": [
        {"ticker": "XLE", "label": "Energy sector exposure"},
    ],
}

def choose_etfs(snapshot: dict) -> list[dict]:
    top_theme = snapshot.get("top_theme", "broad")
    risk_tone = snapshot.get("risk_tone", "neutral")

    if top_theme == "tech":
        return ETF_LIBRARY["tech"][:3]
    if risk_tone == "defensive":
        return ETF_LIBRARY["defensive"][:2] + ETF_LIBRARY["broad"][:1]
    if top_theme == "energy":
        return ETF_LIBRARY["energy"][:1] + ETF_LIBRARY["broad"][:2]

    return ETF_LIBRARY["broad"][:2] + ETF_LIBRARY["defensive"][:1]