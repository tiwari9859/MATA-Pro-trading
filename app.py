import streamlit as st
import yfinance as yf
import requests
import time

TOKEN = "8666809875:AAE_BxvQ0t54uOSTSaujZQmqQnM9gWMkdbg"
CHAT_ID = "8963973514"

def send_msg(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        requests.get(url)
    except:
        pass

def check_signals(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="1h", progress=False)
        if len(df) < 20: return None
        
        df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        
        curr_price = float(df['Close'].iloc[-1])
        ema9 = float(df['EMA9'].iloc[-1])
        ema20 = float(df['EMA20'].iloc[-1])
        
        if (curr_price > ema9) and (ema9 > ema20):
            return f"🚀 BULLISH BTC: Price {curr_price:.2f} > 9EMA"
        if (curr_price < ema20) and (ema9 < ema20):
            return f"📉 BEARISH BTC: Price {curr_price:.2f} < 20EMA"
    except:
        return None
    return None

st.title("Sachin-Pro: Live Status")
if st.button("Activate Trade Bot"):
    st.success("Engine is running...")
    send_msg("Bot Started Successfully!")
    while True:
        signal = check_signals("BTC-USD")
        if signal:
            send_msg(signal)
        time.sleep(60)
