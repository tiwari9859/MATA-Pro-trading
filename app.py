import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

# 1. Sidebar
ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# 2. Data Fetching
df = yf.download(ticker, period="1mo", interval=timeframe)

if not df.empty:
    # Price Fix
    current_price = df['Close'].iloc[-1].item()
    st.metric(label=f"LIVE PRICE: {ticker}", value=f"${current_price:,.2f}")

    # 3. Indicators (EMA)
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    # 4. Chart with EMA & SR lines
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'].squeeze(), high=df['High'].squeeze(),
                    low=df['Low'].squeeze(), close=df['Close'].squeeze())])
    
    # Add EMAs
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='orange', width=1)))
    
    st.plotly_chart(fig, use_container_width=True)

    # 5. News Section
    st.subheader(f"Latest News for {ticker}")
    ticker_obj = yf.Ticker(ticker)
    try:
        news = ticker_obj.news
        for item in news[:5]:
            st.write(f"*{item['title']}* - [Read]({item['link']})")
    except:
        st.write("News filhal load nahi ho rahi.")
else:
    st.error("Data load nahi ho raha.")
