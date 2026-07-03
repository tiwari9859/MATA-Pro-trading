import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Sachin-Trader-Pro Master Terminal")

# 1. Sidebar & Asset Selection
ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# 2. Data Fetching
df = yf.download(ticker, period="1mo", interval=timeframe)

if not df.empty:
    current_price = df['Close'].iloc[-1]
    
    # 3. Display Price
    st.metric(label=f"LIVE PRICE: {ticker}", value=f"${float(current_price):,.2f}")

    # 4. Support/Resistance & Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])])
    st.plotly_chart(fig, use_container_width=True)

    # 5. News Section
    st.subheader(f"Latest News for {ticker}")
    # yfinance mein news ke liye ticker object use hota hai
    ticker_obj = yf.Ticker(ticker)
    news = ticker_obj.news
    
    for item in news[:5]:  # Top 5 news
        st.write(f"*{item['title']}*")
        st.write(f"Source: {item['publisher']} | [Read More]({item['link']})")
        st.write("---")
else:
    st.error("Data load nahi ho raha, thodi der baad try karein.")
