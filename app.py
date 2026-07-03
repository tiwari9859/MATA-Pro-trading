import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Sachin-Trader-Pro Master Terminal")

# 1. Sidebar & Asset Selection
ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# 2. Data Fetching
# Humne period thoda lamba kiya hai taaki data mil sake
df = yf.download(ticker, period="1mo", interval=timeframe)

if not df.empty:
    # Error fix: check kiya ki data hai ya nahi
    current_price = df['Close'].iloc[-1]
    
    # 3. Display Price (Fixed: float check)
    price_to_display = float(current_price) if current_price is not None else 0.0
    st.metric(label=f"LIVE PRICE: {ticker}", value=f"${price_to_display:,.2f}")

    # 4. Support/Resistance & Chart
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'])])
    st.plotly_chart(fig, use_container_width=True)

    # 5. News Section
    st.subheader(f"Latest News for {ticker}")
    ticker_obj = yf.Ticker(ticker)
    try:
        news = ticker_obj.news
        if news:
            for item in news[:5]:
                st.write(f"*{item['title']}*")
                st.write(f"Source: {item['publisher']} | [Read More]({item['link']})")
                st.write("---")
        else:
            st.write("Abhi koi news nahi hai.")
    except Exception as e:
        st.write("News load nahi ho payi.")
else:
    st.error("Data load nahi ho raha, market shayad closed hai ya internet issue hai.")
