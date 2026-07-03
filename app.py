import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Sachin-Trader-Pro Master Terminal")

ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# Data Fetching
try:
    df = yf.download(ticker, period="1mo", interval=timeframe)
    
    # Check if df is not empty and has the required columns
    if not df.empty and 'Close' in df.columns:
        current_price = df['Close'].iloc[-1]
        
        # Display Price
        price_val = float(current_price) if current_price is not None else 0.0
        st.metric(label=f"LIVE PRICE: {ticker}", value=f"${price_val:,.2f}")

        # Chart
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['Open'], high=df['High'],
                        low=df['Low'], close=df['Close'])])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data load nahi ho raha, shayad market data temporary down hai.")
except Exception as e:
    st.error(f"Error: {e}")
