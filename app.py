import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

# Auto-refresh mechanism (30 seconds)
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Sidebar
ticker = st.sidebar.selectbox("Select Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

def get_data(symbol, tf):
    df = yf.download(symbol, period="5d", interval=tf)
    if not df.empty:
        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    return df

# Data Fetch
df = get_data(ticker, timeframe)

if not df.empty:
    current_price = df['Close'].iloc[-1].item()
    ema9 = df['EMA9'].iloc[-1].item()
    ema20 = df['EMA20'].iloc[-1].item()

    # 1. Price & Trend Info
    col1, col2, col3 = st.columns(3)
    col1.metric("LIVE PRICE", f"${current_price:,.2f}")
    
    trend = "BULLISH" if ema9 > ema20 else "BEARISH"
    col2.metric("MARKET TREND", trend)
    col3.metric("RANGE (High-Low)", f"${(df['High'].max() - df['Low'].min()):,.2f}")

    # 2. Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'].iloc[:,0], high=df['High'].iloc[:,0], low=df['Low'].iloc[:,0], close=df['Close'].iloc[:,0])])
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'].iloc[:,0], name='EMA 9', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'].iloc[:,0], name='EMA 20', line=dict(color='orange')))
    st.plotly_chart(fig, use_container_width=True)

    # 3. News
    st.subheader(f"Latest News for {ticker}")
    news = yf.Ticker(ticker).news
    for item in news[:5]:
        st.write(f"*{item['title']}* - [Read More]({item['link']})")

    # Auto Refresh logic
    time.sleep(30)
    st.rerun()
else:
    st.error("Data load nahi ho raha.")
