import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import feedparser
from streamlit_autorefresh import st_autorefresh

# Page setup
st.set_page_config(layout="wide")
st_autorefresh(interval=30000, key="datarefresh")

st.title("📈 M.A.T.A Pro - Advanced Trading Terminal")

# Session State (Setting save rakhne ke liye)
if 'ticker' not in st.session_state: st.session_state.ticker = 'BTC-USD'
if 'timeframe' not in st.session_state: st.session_state.timeframe = '1h'

# Sidebar
st.session_state.ticker = st.sidebar.text_input("Enter Asset", st.session_state.ticker)
st.session_state.timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "4h"], index=["1d", "1h", "4h"].index(st.session_state.timeframe))

# Data Download
data = yf.download(st.session_state.ticker, period="5d", interval=st.session_state.timeframe)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Price Card (Bada Price)
current_price = data['Close'].iloc[-1]
st.metric(label=f"LIVE PRICE: {st.session_state.ticker}", value=f"${current_price:,.2f}")

# EMA Calculation
data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()

# Chart (Sirf chart area update hoga)
fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Market')])
fig.add_trace(go.Scatter(x=data.index, y=data['EMA9'], name='EMA 9', line=dict(color='yellow', width=1.5)))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], name='EMA 20', line=dict(color='blue', width=1.5)))
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Signal
if data['EMA9'].iloc[-1] > data['EMA20'].iloc[-1]:
    st.success("Signal: BULLISH (EMA 9 > EMA 20)")
else:
    st.error("Signal: BEARISH (EMA 9 < EMA 20)")

# News
st.subheader("📰 Latest Crypto Market News")
try:
    news_feed = feedparser.parse("https://cointelegraph.com/rss")
    for entry in news_feed.entries[:3]:
        st.write(f"🔹 *{entry.title}*")
except:
    st.write("News load nahi ho rahi.")
