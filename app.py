import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

# Sidebar
ticker = st.sidebar.selectbox("Select Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# Data Fetching
@st.cache_data(ttl=30)
def get_data(symbol, tf):
    df = yf.download(symbol, period="5d", interval=tf)
    # Data fix for new yfinance format
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    if not df.empty:
        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df

df = get_data(ticker, timeframe)

if not df.empty:
    current_price = float(df['Close'].iloc[-1])
    ema9 = float(df['EMA9'].iloc[-1])
    ema20 = float(df['EMA20'].iloc[-1])
    market_range = float(df['High'].max() - df['Low'].min())

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("LIVE PRICE", f"${current_price:,.2f}")
    col2.metric("MARKET TREND", "BULLISH" if ema9 > ema20 else "BEARISH")
    col3.metric("RANGE (High-Low)", f"${market_range:,.2f}")

    # Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='orange')))
    st.plotly_chart(fig, use_container_width=True)

    # News (Safe access)
    st.subheader(f"Latest News for {ticker}")
    ticker_obj = yf.Ticker(ticker)
    news_list = ticker_obj.get_news()
    
    if news_list:
        for item in news_list[:5]:
            title = item.get('title', 'News unavailable')
            link = item.get('link', '#')
            st.write(f"*{title}* - [Read More]({link})")
    else:
        st.write("Abhi koi news nahi hai.")

    # Auto-refresh
    time.sleep(30)
    st.rerun()
else:
    st.error("Data load nahi ho raha, market shayad band hai.")
