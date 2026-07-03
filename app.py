import streamlit as st
import streamlit.components.v1 as components
import feedparser
import yfinance as yf
import pandas as pd

# Page setup
st.set_page_config(layout="wide", page_title="Sachin-Trader-Pro")
st.title("📈 Sachin-Trader-Pro Trading Terminal")

ticker = st.sidebar.text_input("Enter Asset (e.g. BTC-USD)", "BTC-USD")

# 1. EMA Logic aur Signal ke liye Data Fetching
df = yf.download(ticker, period="5d", interval="1h")
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

# 2. Automated Signal
current_ema9 = df['EMA9'].iloc[-1]
current_ema20 = df['EMA20'].iloc[-1]

st.subheader("🤖 AI Trading Signal (9/20 EMA Strategy)")
if current_ema9 > current_ema20:
    st.success("✅ BULLISH: EMA 9 upar hai! BUY/LONG ka setup dekhein.")
else:
    st.error("❌ BEARISH: EMA 20 upar hai! SELL/SHORT ka setup dekhein.")

# 3. TradingView Chart
chart_html = f"""
<div class="tradingview-widget-container">
  <div id="tradingview_chart"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
  "width": "100%", "height": 500, "symbol": "BINANCE:{ticker.replace('-', '')}",
  "interval": "60", "theme": "dark", "style": "1", "container_id": "tradingview_chart"
  }});
  </script>
</div>
"""
components.html(chart_html, height=550)

# News Section
st.subheader("📰 Latest Crypto Market News")
try:
    news_feed = feedparser.parse("https://cointelegraph.com/rss")
    for entry in news_feed.entries[:3]:
        st.write(f"🔹 *{entry.title}*")
except:
    st.write("News feed unavailable.")
