import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests
import feedparser

# Telegram Alert Function
def send_telegram_alert(message):
    token = "8666809875:AAE_BxvQ0t54uOSTSaujZQmqQnM9gWMkdbg" 
    chat_id = "8963973514"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

st.set_page_config(layout="wide")
st.title("📈 Sachin-Trader-Pro Master Terminal")

# Sidebar - Timeframe ke neeche News
ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
tf = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

st.sidebar.subheader("📰 Latest Market News")
try:
    news_feed = feedparser.parse("https://cointelegraph.com/rss")
    for entry in news_feed.entries[:3]:
        st.sidebar.caption(f"🔹 {entry.title}")
except:
    st.sidebar.write("News feed unavailable.")

# Data Fetching
df = yf.download(ticker, period="5d", interval=tf)
if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

# Calculations
df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

# S&R
pivot = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
support = pivot - (df['High'].iloc[-2] - df['Low'].iloc[-2])
resistance = pivot + (df['High'].iloc[-2] - df['Low'].iloc[-2])

# Price & Signal
current_price = df['Close'].iloc[-1]
st.metric(label=f"LIVE PRICE: {ticker}", value=f"${current_price:,.2f}")

# Alert & Signal Logic
if 'last_status' not in st.session_state: st.session_state.last_status = None
current_status = "BULLISH" if df['EMA9'].iloc[-1] > df['EMA20'].iloc[-1] else "BEARISH"
is_high_volume = df['Volume'].iloc[-1] > df['Vol_Avg'].iloc[-1]

if st.session_state.last_status is not None and st.session_state.last_status != current_status and is_high_volume:
    msg = f"🚀 SETUP BAN GAYA! {ticker} {current_status}. Target: {resistance if current_status=='BULLISH' else support:.2f}"
    send_telegram_alert(msg)
st.session_state.last_status = current_status

# Main Chart (Pro Look)
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='#FFD700', width=2)))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='#1E90FF', width=2)))
fig.update_layout(height=600, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

# Footer Setup info
col1, col2, col3 = st.columns(3)
col1.metric("Status", current_status)
col2.metric("Support", f"${support:.2f}")
col3.metric("Resistance", f"${resistance:.2f}")
