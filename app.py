import streamlit as st
import yfinance as yf
import pandas as pd

# Page setup
st.set_page_config(page_title="Sachin-Pro", layout="wide")
st.title("📈 Sachin-Pro: Live Trading Desk")

# 1. Data Fetching
@st.cache_data(ttl=60)
def get_data():
    df = yf.download("BTC-USD", period="1d", interval="1h", progress=False)
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df

df = get_data()
curr_price = float(df['Close'].iloc[-1])

# 2. Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Live Price", f"${curr_price:,.2f}")
c2.metric("9 EMA", f"{df['EMA9'].iloc[-1]:.2f}")
c3.metric("20 EMA", f"{df['EMA20'].iloc[-1]:.2f}")

# 3. Chart
st.subheader("Live Market Trend (1H)")
st.line_chart(df[['Close', 'EMA9', 'EMA20']])

# 4. Market Updates
st.subheader("📰 Market Updates")
st.write("• Strategy: 9/20 EMA Crossover Monitoring")
st.write("• Timeframe: 1 Hour")
st.write("• Status: Dashboard is live and tracking market movement.")
