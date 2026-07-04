import streamlit as st
import yfinance as yf
import requests
import time

# Telegram Settings
TOKEN = "8666809875:AAE_BxvQ0t54uOSTSaujZQmqQnM9gWMkdbg"
CHAT_ID = "8963973514"

st.title("🔥 Sachin-Pro: Simple Bot")

# Engine
if st.button("Start"):
    st.write("Bot is running...")
    while True:
        try:
            df = yf.download("BTC-USD", period="5d", interval="1h", progress=False)
            df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            
            curr = float(df['Close'].iloc[-1])
            e9 = float(df['EMA9'].iloc[-1])
            e20 = float(df['EMA20'].iloc[-1])
            
            # Logic
            if e9 > e20 and curr > e9:
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚀 BUY SIGNAL: BTC {curr:.2f}")
            elif e9 < e20 and curr < e20:
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=📉 SELL SIGNAL: BTC {curr:.2f}")
            
            time.sleep(3600) # Wait 1 hour
        except:
            time.sleep(60) # Agar error aaye toh 1 min baad fir koshish karega
