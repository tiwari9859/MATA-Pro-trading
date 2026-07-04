import streamlit as st
import yfinance as yf
import requests
import time

# Aapki Telegram Details
TOKEN = "8666809875:AAE_BxvQ0t54uOSTSaujZQmqQnM9gWMkdbg"
CHAT_ID = "8963973514"

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)

def calculate_trade_levels(df, type):
    last_row = df.iloc[-1]
    # Risk Reward 1:2 logic
    if type == "BUY":
        sl = last_row['Low'] - (last_row['Close'] * 0.003)
        tp = last_row['Close'] + ((last_row['Close'] - sl) * 2)
        return sl, tp
    else:
        sl = last_row['High'] + (last_row['Close'] * 0.003)
        tp = last_row['Close'] - ((sl - last_row['Close']) * 2)
        return sl, tp

def check_signals(ticker):
    df = yf.download(ticker, period="10d", interval="1h")
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    # Pivot calculation for S&R
    p = (df['High'].iloc[-2] + df['Low'].iloc[-2] + df['Close'].iloc[-2]) / 3
    s1 = (2 * p) - df['High'].iloc[-2]
    r1 = (2 * p) - df['Low'].iloc[-2]
    
    curr_price = df['Close'].iloc[-1]
    ema9 = df['EMA9'].iloc[-1]
    ema20 = df['EMA20'].iloc[-1]
    
    # BULLISH LOGIC: Price > 9EMA and 9EMA > 20EMA + Near Support
    if (curr_price > ema9) and (ema9 > ema20):
        if curr_price <= r1 + (r1 * 0.002):
            sl, tp = calculate_trade_levels(df, "BUY")
            return f"🚀 BULLISH SETUP: {ticker}\nEntry: {curr_price:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}\nLogic: Price > 9EMA & Support Zone"
            
    # BEARISH LOGIC: Price < 20EMA and 9EMA < 20EMA + Near Resistance
    if (curr_price < ema20) and (ema9 < ema20):
        if curr_price >= s1 - (s1 * 0.002):
            sl, tp = calculate_trade_levels(df, "SELL")
            return f"📉 BEARISH SETUP: {ticker}\nEntry: {curr_price:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}\nLogic: Price < 20EMA & Resistance Zone"
            
    return None

st.title("🔥 Sachin-Pro: Advanced Signal Engine")
if st.button("Activate Trade Bot"):
    st.write("Engine running... monitoring 1H Timeframe...")
    while True:
        signal = check_signals("BTC-USD")
        if signal:
            send_msg(signal)
            st.success(signal)
        time.sleep(10) # 10 second mein check karega
