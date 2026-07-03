import streamlit as st
import yfinance as yf
st.title("📈 M.A.T.A Pro - AI Trading Tool")
ticker = st.sidebar.text_input("Enter Asset", "BTC-USD")
data = yf.download(ticker, period="1mo", interval="1d")
st.subheader("Price Chart")
st.line_chart(data['Close'])
if st.button("Analyze Now"):
    st.write("Processing... AI Model Active!")
