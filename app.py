import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# Data Fetching
df = yf.download(ticker, period="1mo", interval=timeframe)

if not df.empty:
    # Yahan fix hai: .iloc[-1] ke baad .item() lagane se wo sirf number lega, series nahi
    current_price = df['Close'].iloc[-1].item() 
    
    st.metric(label=f"LIVE PRICE: {ticker}", value=f"${current_price:,.2f}")

    # Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'].squeeze(), 
                    high=df['High'].squeeze(),
                    low=df['Low'].squeeze(), 
                    close=df['Close'].squeeze())])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Data abhi load nahi ho raha hai.")
