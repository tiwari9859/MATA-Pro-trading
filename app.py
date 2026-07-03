import streamlit as st
import streamlit.components.v1 as components
import feedparser

# Page configuration
st.set_page_config(layout="wide", page_title="Sachin-Trader-Pro")

st.title("📈 Sachin-Trader-Pro Trading Terminal")

# Sidebar for Asset Selection
ticker = st.sidebar.text_input("Enter Asset (e.g. BTCUSDT)", "BTCUSDT")

# TradingView Widget Section
st.subheader("📊 Live Interactive Trading Chart")

chart_html = f"""
<div class="tradingview-widget-container">
  <div id="tradingview_chart"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
  "width": "100%",
  "height": 600,
  "symbol": "BINANCE:{ticker}",
  "interval": "60",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "allow_symbol_change": true,
  "container_id": "tradingview_chart"
  }});
  </script>
</div>
"""

# Render the chart
components.html(chart_html, height=650)

st.info("💡 Aap is chart par tools, indicators aur alerts set kar sakte hain.")

# News Section
st.subheader("📰 Latest Crypto Market News")
try:
    news_feed = feedparser.parse("https://cointelegraph.com/rss")
    for entry in news_feed.entries[:3]:
        st.write(f"🔹 *{entry.title}*")
        st.caption(f"Time: {entry.published}")
except:
    st.write("News feed load nahi ho rahi.")
