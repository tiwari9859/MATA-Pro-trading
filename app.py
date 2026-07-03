import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")
st.title("Sachin-Trader-Pro Master Terminal")

# Sidebar
ticker = st.sidebar.selectbox("Select Asset", ["BTC-USD", "ETH-USD"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1h", "4h", "1d"])

# Sidebar News
st.sidebar.subheader("Latest News")
ticker_obj = yf.Ticker(ticker)
news = ticker_obj.news
for item in news[:5]:
    st.sidebar.markdown(f"[{item.get('title', 'Read News')}]({item.get('link', '#')})")

@st.cache_data(ttl=30)
def get_data(symbol, tf):
    df = yf.download(symbol, period="1mo", interval=tf)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df['EMA9'] = df['Close'].ewm(span=9, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = (2 * df['Pivot']) - df['Low']
    df['S1'] = (2 * df['Pivot']) - df['High']
    return df

df = get_data(ticker, timeframe)

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("LIVE PRICE", f"${float(df['Close'].iloc[-1]):,.2f}")
    col2.metric("MARKET TREND", "BULLISH" if df['EMA9'].iloc[-1] > df['EMA20'].iloc[-1] else "BEARISH")
    col3.metric("RANGE (High-Low)", f"${float(df['High'].max() - df['Low'].min()):,.2f}")

    # TradingView Style Chart
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
    )])
    
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA 9', line=dict(color='#2962ff', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name='EMA 20', line=dict(color='#ff6d00', width=1.5)))
    fig.add_trace(go.Scatter(x=df.index, y=df['R1'], name='Resistance', line=dict(color='#ef5350', width=1, dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['S1'], name='Support', line=dict(color='#26a69a', width=1, dash='dash')))
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        yaxis=dict(side="right", title="Price"),
        height=600,
        uirevision='constant',
        margin=dict(l=10, r=50, t=30, b=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Auto-update
    time.sleep(10)
    st.rerun()
