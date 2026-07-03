def check_signals(ticker):
    df = yf.download(ticker, period="10d", interval="1h")
    # Yahan hum memastikan kar rahe hain ki data sahi format mein hai
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    # Pivot logic ko fix kiya taaki error na aaye
    last_idx = -1
    prev_idx = -2
    
    curr_price = float(df['Close'].iloc[last_idx])
    ema9 = float(df['EMA9'].iloc[last_idx])
    ema20 = float(df['EMA20'].iloc[last_idx])
    
    # Pivot points calculate karte waqt .item() use karenge taaki value error na ho
    high_prev = float(df['High'].iloc[prev_idx])
    low_prev = float(df['Low'].iloc[prev_idx])
    close_prev = float(df['Close'].iloc[prev_idx])
    
    p = (high_prev + low_prev + close_prev) / 3
    s1 = (2 * p) - high_prev
    r1 = (2 * p) - low_prev
    
    # Logic
    if (curr_price > ema9) and (ema9 > ema20):
        if curr_price <= r1 + (r1 * 0.002):
            sl, tp = calculate_trade_levels(df, "BUY")
            return f"🚀 BULLISH SETUP: {ticker}\nEntry: {curr_price:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}"
            
    if (curr_price < ema20) and (ema9 < ema20):
        if curr_price >= s1 - (s1 * 0.002):
            sl, tp = calculate_trade_levels(df, "SELL")
            return f"📉 BEARISH SETUP: {ticker}\nEntry: {curr_price:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}"
            
    return None
