import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

ticker = st.sidebar.selectbox("Select Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# Sidebar News Fix
st.sidebar.subheader("Latest News")
ticker_obj = yf.Ticker(ticker)
news = ticker_obj.news
for item in news[:5]:
    st.sidebar.markdown(f"[{item.get('title', 'Read News')}]({item.get('link', '#')})")

@st.cache_data(ttl=60)
def get_data(symbol, tf):
    df = yf.download(symbol, period="1mo", interval=tf)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    # Indicators
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    # Support/Resistance Calculation
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = (2 * df['Pivot']) - df['Low']
    df['S1'] = (2 * df['Pivot']) - df['High']
    return df

df = get_data(ticker, timeframe)

if not df.empty:
    current_price = float(df['Close'].iloc[-1])
    ema9 = float(df['EMA9'].iloc[-1])
    ema20 = float(df['EMA20'].iloc[-1])
    market_range = float(df['High'].max() - df['Low'].min())

    col1, col2, col3 = st.columns(3)
    col1.metric("LIVE PRICE", f"${current_price:,.2f}")
    col2.metric("MARKET TREND", "BULLISH" if ema9 > ema20 else "BEARISH")
    col3.metric("RANGE (High-Low)", f"${market_range:,.2f}")

    # Zoom fix: uirevision use kiya hai
    fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        yaxis=dict(side="right", title="Price"),
        height=600,
        uirevision='dataset' 
    )
    
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='orange', width=1)))
    # Support & Resistance Lines
    fig.add_trace(go.Scatter(x=df.index, y=df['R1'], name='Resistance', line=dict(color='red', width=1, dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['S1'], name='Support', line=dict(color='green', width=1, dash='dash')))
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Refresh Terminal"):
        st.rerun()
else:
    st.error("Data load nahi ho raha.")
