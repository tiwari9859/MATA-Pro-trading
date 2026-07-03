import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import requests

# Telegram Alert Function
def send_telegram_alert(message):
    token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

st.set_page_config(layout="wide")
st.title("📈 Sachin-Trader-Pro: Advanced Setup")

# Data Fetching
ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
df = yf.download(ticker, period="5d", interval="1h")
if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

# Calculations
df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

# Support & Resistance (Pivot Points)
pivot = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
support = pivot - (df['High'].iloc[-2] - df['Low'].iloc[-2])
resistance = pivot + (df['High'].iloc[-2] - df['Low'].iloc[-2])

# Logic with Volume & Support/Resistance
current_vol = df['Volume'].iloc[-1]
avg_vol = df['Vol_Avg'].iloc[-1]
is_high_volume = current_vol > avg_vol

# Signal Alert
if df['EMA9'].iloc[-1] > df['EMA20'].iloc[-1] and is_high_volume:
    st.success(f"🚀 BUY SIGNAL! High Volume Breakout. Resistance Target: ${resistance:.2f}")
elif df['EMA9'].iloc[-1] < df['EMA20'].iloc[-1] and is_high_volume:
    st.error(f"⚠️ SELL SIGNAL! High Volume Drop. Support Target: ${support:.2f}")

# Chart
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Market'))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='yellow')))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='blue')))
st.plotly_chart(fig, use_container_width=True)

st.write(f"📊 *Volume Check*: {'HIGH (Volume confirmed)' if is_high_volume else 'LOW (Wait for volume)'}")
st.write(f"🎯 *Support: ${support:.2f} | **Resistance*: ${resistance:.2f}")
