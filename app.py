import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import feedparser
from streamlit_autorefresh import st_autorefresh

# Page setup
st.set_page_config(layout="wide", page_title="Sachin-Trader-Pro")

# 30 second auto-refresh
st_autorefresh(interval=30000, key="datarefresh")

st.title("📈 Sachin-Trader-Pro Trading Terminal")

# Sidebar
ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "4h"])

# Data Download
data = yf.download(ticker, period="5d", interval=timeframe)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Price Metric
current_price = data['Close'].iloc[-1]
st.metric(label=f"LIVE PRICE: {ticker}", value=f"${current_price:,.2f}")

# EMA Calculation
data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()

# Chart
fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Market')])
fig.add_trace(go.Scatter(x=data.index, y=data['EMA9'], name='EMA 9', line=dict(color='yellow', width=2)))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], name='EMA 20', line=dict(color='blue', width=2)))
fig.update_layout(height=600, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Signal Logic
st.subheader("🤖 AI Trading Signal")
if data['EMA9'].iloc[-1] > data['EMA20'].iloc[-1]:
    st.success("✅ BULLISH: EMA 9 > EMA 20 (Look for BUY opportunities)")
else:
    st.error("❌ BEARISH: EMA 9 < EMA 20 (Look for SELL opportunities)")

# News Section
st.subheader("📰 Latest Crypto Market News")
try:
    news_feed = feedparser.parse("https://cointelegraph.com/rss")
    for entry in news_feed.entries[:3]:
        st.write(f"🔹 *{entry.title}*")
except:
    st.write("News load nahi ho rahi.")
