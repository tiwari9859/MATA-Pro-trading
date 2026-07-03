import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page setup
st.set_page_config(layout="wide")

# Har 30 second mein refresh (Auto-update)
st_autorefresh(interval=30000, key="datarefresh")

st.title("📈 M.A.T.A Pro - Advanced Trading Terminal")

# Sidebar settings
ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "4h"])

# Data download
data = yf.download(ticker, period="5d", interval=timeframe)

# Data Fix (Multi-index handling)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# EMA Calculation
data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()

# Candlestick Chart
fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'], name='Market')])

# Add EMA lines
fig.add_trace(go.Scatter(x=data.index, y=data['EMA9'], name='EMA 9', line=dict(color='yellow', width=1.5)))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], name='EMA 20', line=dict(color='blue', width=1.5)))

st.plotly_chart(fig, use_container_width=True)

# Signal Logic
if data['EMA9'].iloc[-1] > data['EMA20'].iloc[-1]:
    st.success("Signal: BULLISH (EMA 9 > EMA 20)")
else:
    st.error("Signal: BEARISH (EMA 9 < EMA 20)")

st.write("---")
st.caption("Auto-refreshing every 30 seconds for live monitoring.")
