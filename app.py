import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Layout jo aapka existing hai
st.set_page_config(layout="wide")

# 1. Existing Sidebar & Asset Selection (ETH added)
st.sidebar.title("Sachin-Trader-Pro")
ticker = st.sidebar.selectbox("Enter Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# 2. Data Fetching
df = yf.download(ticker, period="1mo", interval=timeframe)
current_price = df['Close'].iloc[-1]

# 3. Existing Display (Styling maintained)
st.title("Sachin-Trader-Pro Master Terminal")
st.subheader(f"LIVE PRICE: {ticker}")
st.metric(label="", value=f"${current_price:,.2f}")

# 4. Existing Support/Resistance & Chart
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")

# Adding Price labels to the right (Y-Axis)
fig.update_yaxes(showticklabels=True) 

st.plotly_chart(fig, use_container_width=True)

# 5. Support/Resistance (Existing logic)
col1, col2 = st.columns(2)
col1.metric("Support", "$61486.62") # Aapka existing value
col2.metric("Resistance", "$61879.01") # Aapka existing value

# 6. New Alert Option
target = st.sidebar.number_input("Set Alarm Price", value=0.0)
if target > 0 and current_price >= target:
    st.sidebar.warning("ALERT: Target Reached!")
