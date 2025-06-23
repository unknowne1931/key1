import yfinance as yf
import pandas as pd
from newsapi import NewsApiClient
import webbrowser, os

# --- Config ---
ASSETS = {
  "Large Cap": ['RELIANCE.NS','TCS.NS','INFY.NS'],
  "Small Cap": ['JAMNAAUTO.NS','NILKAMAL.NS'],
  "New‑Age Stocks": ['ZOMATO.NS','PAYTM.NS'],
  "Commodities": ['CL=F','GC=F'],
  "Forex": ['INR=X','EURINR=X'],
  "Crypto": ['BTC-USD','ETH-USD']
}
UP_MOVE, DOWN_MOVE = 0.10, -0.10
NEWS_KEY = "YOUR_NEWSAPI_KEY"

# --- Fetch Prices + Risk Calculations ---
rows = []
for cat, tickers in ASSETS.items():
    for sym in tickers:
        try:
            hist = yf.Ticker(sym).history(period="5d")['Close']
            entry = hist.iloc[-1]
            target = entry*(1+UP_MOVE)
            stop = entry*(1+DOWN_MOVE)
            rr = (target-entry)/(entry-stop)
        except:
            entry, target, stop, rr = [None]*4
        rows.append({"Category":cat, "Symbol":sym,
                     "Entry":entry, "Target":target,
                     "Stop":stop, "R/R":rr})

df_prices = pd.DataFrame(rows)

# --- Fetch News + Compute Simple Sentiment ---
newsapi = NewsApiClient(api_key=NEWS_KEY)
def get_sentiment(symbol):
    try:
        arts = newsapi.get_everything(q=symbol, language='en', sort_by='publishedAt', page_size=5)
        titles = [a['title'] for a in arts['articles']]
    except:
        return "Neutral"
    score = sum((title.lower().count(w) for title in titles for w in ["gain","surge","rise","drop","dip","fall","profit","loss"] ))
    return "Likely Profit" if score>1 else ("Likely Loss" if score< -1 else "Neutral")

df_prices['NewsSent'] = df_prices['Symbol'].apply(get_sentiment)

# --- Build HTML Dashboard ---
df_prices = df_prices.round(2)
html = df_prices.to_html(index=False, classes='table')

template = f"""
<html><head><title>All‑Market Trade & News Dashboard</title>
<style>
body{{font-family:Arial;padding:20px;background:#f4f4f4}}
h2{{text-align:center}}
.table{{width:95%;margin:auto;border-collapse:collapse}}
.table th,td{{border:1px solid #ddd;padding:8px;text-align:center}}
.table th{{background:#333;color:#fff}}
td:nth-child(3),td:nth-child(4),td:nth-child(5){{white-space:nowrap}}
</style></head><body>
<h2>📊 Trade Risk & News Sentiment</h2>{html}</body></html>
"""

file = "trade_news_dashboard.html"
with open(file,"w",encoding="utf-8") as f:
    f.write(template)
webbrowser.open('file://' + os.path.realpath(file))
