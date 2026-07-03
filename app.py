import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")
st.title("📈 M.A.T.A Pro - Advanced Trading Terminal")

ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
timeframe = st.sidebar.selectbox("Select Timeframe", ["1d", "1h", "4h"])

# Data Download
data = yf.download(ticker, period="1mo", interval=timeframe)

# Data Fix (Multi-index handling)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# EMA Calculation
data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()

# Interactive Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='white')))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA9'], name='EMA 9', line=dict(color='yellow')))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], name='EMA 20', line=dict(color='blue')))

st.plotly_chart(fig, use_container_width=True)

# Signal Logic
if data['EMA9'].iloc[-1] > data['EMA20'].iloc[-1]:
    st.success("Signal: BULLISH (EMA 9 > EMA 20)")
else:
    st.error("Signal: BEARISH (EMA 9 < EMA 20)")
